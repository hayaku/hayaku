# -*- coding: utf-8 -*-
# (c) 2012 Sergey Mezentsev
import re
import string
import copy

from itertools import chain, product, starmap


def parse_dict_json(raw_dict):
    result_dict = {}

    valuable = (i for i in raw_dict if 'name' in i and 'values' in i)

    def strip(s):
        return string.strip(s) if hasattr(string, 'strip') else s.strip()

    for i in valuable:
        name, values, default, always_positive, remove_values, _type = i['name'], i['values'], i.get('default'), i.get('always_positive'), i.get('remove_values'), i.get('type')
        names = name if isinstance(name, list) else map(strip, name.split(','))
        for n in names:
            assert n not in result_dict

            new_values = []
            for subval in values:
                # Is there a better symbol/symbols for space replacement
                # than ~?
                new_values.append(subval.replace(' ', '~'))
            val = { 'values': new_values }

            if default is not None:
                val['default'] = default

            if remove_values is not None:
                val['remove_values'] = remove_values

            if always_positive is not None:
                val['always_positive'] = always_positive

            if _type is not None:
                val['type'] = _type

            if 'prefixes' in i:
                val['prefixes'] = i['prefixes']
                if 'no_unprefixed_property' in i:
                    val['no_unprefixed_property'] = i['no_unprefixed_property']
            else:
                assert 'no_unprefixed_property' not in i

            result_dict[n] = val

    return result_dict

def merge_aliases(initial_left_aliases, initial_right_aliases):
    left_aliases = copy.deepcopy(initial_left_aliases)
    right_aliases = copy.deepcopy(initial_right_aliases)

    for rname in right_aliases:
        left_aliases[rname] = right_aliases[rname]

    return left_aliases

def merge_dict(initial_left_dict, initial_right_dict):
    left_dict = copy.deepcopy(initial_left_dict)
    right_dict = copy.deepcopy(initial_right_dict)
    if isinstance(left_dict, list):
        left_dict = parse_dict_json(left_dict)

    if isinstance(right_dict, list):
        right_dict = parse_dict_json(right_dict)

    #1
    for rname in right_dict:
        if rname not in left_dict:
            left_dict[rname] = right_dict[rname]
            continue
        #3
        for value in ['default', 'prefixes', 'no_unprefixed_property', 'always_positive', 'type']:
            if value in right_dict[rname]:
                left_dict[rname][value] = right_dict[rname][value]

        #4
        if 'values' in right_dict[rname]:
            old_vals = [ov for ov in left_dict[rname]['values'] if ov not in right_dict[rname]['values']]
            new_vals = right_dict[rname]['values']
            if '...' in right_dict[rname]['values']:
                split_index = new_vals.index('...')
                new_vals = new_vals[:split_index] + old_vals + new_vals[split_index+1:]
            else:
                new_vals.extend(old_vals)

            left_dict[rname]['values'] = []
            for k in new_vals:
                if k not in left_dict[rname]['values']:
                    left_dict[rname]['values'].append(k)

        #5
        if 'remove_values' in right_dict[rname]:
            for rv in right_dict[rname]['remove_values']:
                left_dict[rname]['values'] = [i for i in left_dict[rname]['values'] if i != rv]

    return left_dict

def read_file_dictionary():
    CSS_DICT_DIR = 'dictionaries'
    CSS_DICT_FILENAME = 'hayaku_CSS_dictionary.json'
    import json
    import os
    try:
        # TODO: заменить на простой json # ld load_resources
        import sublime
        hayaku_dict = sublime.load_settings(CSS_DICT_FILENAME)
        if hayaku_dict is None:
            import zipfile
            zf = zipfile.ZipFile(os.path.dirname(os.path.realpath(__file__)))
            f = zf.read('{0}/{1}'.format(CSS_DICT_DIR, CSS_DICT_FILENAME))
            hayaku_dict = json.loads(f.decode())
    except ImportError:
        css_dict_path = os.path.join(CSS_DICT_DIR, CSS_DICT_FILENAME)
        if not os.path.exists(css_dict_path):
            css_dict_path = os.path.join(os.path.dirname(__file__), css_dict_path)
        with open(css_dict_path) as f:
            hayaku_dict = json.load(f)
    return hayaku_dict

get_css_dict_cache = {}
def get_css_dict(force_update=False, preprocessor=None):
    global get_css_dict_cache
    css_aliases = {}
    cache_key = 'CSS'

    if preprocessor:
        cache_key = preprocessor

    if cache_key in get_css_dict_cache and not force_update:
        return get_css_dict_cache[cache_key]
    else:
        hayaku_dict = read_file_dictionary()
        css_dict = parse_dict_json(hayaku_dict.get('CSS', {}))
        css_aliases = hayaku_dict.get('CSS_aliases', {})

        if preprocessor:
            preprocessor_dict = parse_dict_json(hayaku_dict.get(preprocessor, {}))
            preprocessor_aliases = hayaku_dict.get(preprocessor + '_aliases', {})
            if preprocessor_dict:
                css_dict = merge_dict(css_dict, preprocessor_dict)
            if preprocessor_aliases:
                css_aliases = merge_dict(css_aliases, preprocessor_aliases)

        assert css_dict is not None
        get_css_dict_cache[cache_key] = (css_dict, css_aliases)
        return get_css_dict_cache[cache_key]

def get_key_from_property(prop, key, css_dict=None, include_commented=False):
    """Returns the entry from the dictionary using the given key"""
    if css_dict is None:
        css_dict = get_css_dict()[0]

    cur = css_dict.get(prop) or css_dict.get(prop[1:-1])
    if cur is None:
        return None
    value = cur.get(key)
    if value is not None:
        return value
    for v in cur['values']:
        if (v.startswith('<') or (include_commented and v.startswith('<_'))) and v.endswith('>'):
            ret = get_key_from_property(v, key, css_dict, include_commented)
            if ret is not None:
                return ret

def css_defaults(name, css_dict=None):
    """Находит первое значение по-умолчанию
    background -> #FFF
    color -> #FFF
    content -> ""
    """
    if css_dict is None:
        css_dict = get_css_dict()[0]

    return get_key_from_property(name, 'default', css_dict)

def css_flat(name, css_dict=None, values=None, include_commented=False):
    """Все значения у свойства (по порядку)
    left -> [u'auto', u'<dimension>', u'<number>', u'<length>', u'.em', u'.ex',
            u'.vw', u'.vh', u'.vmin', u'.vmax', u'.ch', u'.rem', u'.px', u'.cm',
            u'.mm', u'.in', u'.pt', u'.pc', u'<percentage>', u'.%']
    """
    if css_dict is None:
        css_dict = get_css_dict()[0]

    if name.startswith('<') and name.endswith('>'):
        if name.startswith('<_') and include_commented:
            cur = css_dict.get(name.replace('<_', '<')) or css_dict.get(name[2:-1])
        else:
            cur = css_dict.get(name) or css_dict.get(name[1:-1])
    else:
        cur = css_dict.get(name)

    if values is None:
        values = []
    if cur is None:
        return values
    if type(cur) == str: # TODO: исправить проблему с unicode в python 2
        values.append(cur)
        return values
    for value in cur['values']:
        values.append(value)
        if (value.startswith('<') or (include_commented and value.startswith('<_'))) and value.endswith('>'):
            values = css_flat(value, css_dict, values, include_commented)
    return values

def css_flat_list(name, css_dict=None, include_commented=False):
    """Возвращает список кортежей (свойство, возможное значение)
    left -> [(left, auto), (left, <integer>), (left, .px)...]
    """
    if css_dict is None:
        css_dict = get_css_dict()[0]
    return list(product((name,), css_flat(name, css_dict, include_commented=include_commented)))

def get_flat_css(css_dict=None, include_commented=False):
    if css_dict is None:
        css_dict = get_css_dict()[0]

    return list(chain.from_iterable(starmap(css_flat_list, ((i, css_dict, include_commented) for i in css_dict))))

def get_values_by_property(prop, css_dict=None, include_commented=False):
    if css_dict is None:
        css_dict = get_css_dict()[0]
    values = [v for p, v in get_flat_css(css_dict, include_commented) if p == prop and re.match(r'^[a-z-]+$', v)]
    # Return only unique items
    unique_value = list()
    for value in values:
        if value not in unique_value:
            unique_value.append(value)
    return unique_value
