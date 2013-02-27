# -*- coding: utf-8 -*-
# (c) 2012 Sergey Mezentsev
import string

from itertools import chain, product, starmap


def parse_dict_json(raw_dict):
    result_dict = {}

    valuable = (i for i in raw_dict if 'name' in i and 'values' in i)

    def strip(s):
        return string.strip(s) if hasattr(string, 'strip') else s.strip()

    for i in valuable:
        name, values, default = i['name'], i['values'], i.get('default')
        names = name if isinstance(name, list) else map(strip, name.split(','))
        for n in names:
            assert n not in result_dict

            val = { 'values': values }

            if default is not None:
                val['default'] = default

            if 'prefixes' in i:
                val['prefixes'] = i['prefixes']
                if 'no-unprefixed-property' in i:
                    val['no-unprefixed-property'] = i['no-unprefixed-property']
            else:
                assert 'no-unprefixed-property' not in i

            result_dict[n] = val

    return result_dict

get_css_dict_cache = None
def get_css_dict():
    global get_css_dict_cache
    if get_css_dict_cache is not None:
        return get_css_dict_cache
    else:
        CSS_DICT_DIR = 'dictionaries'
        CSS_DICT_FILENAME = 'hayaku_CSS_dictionary.json'
        DICT_KEY = 'hayaku_CSS_dictionary'

        import json
        import os
        try:
            import sublime
            css_dict = sublime.load_settings(CSS_DICT_FILENAME).get(DICT_KEY)
            if css_dict is None:
                import zipfile
                zf = zipfile.ZipFile(os.path.dirname(os.path.realpath(__file__)))
                f = zf.read('{0}/{1}'.format(CSS_DICT_DIR, CSS_DICT_FILENAME))
                css_dict = json.loads(f.decode())[DICT_KEY]
        except ImportError:
            css_dict_path = os.path.join(CSS_DICT_DIR, CSS_DICT_FILENAME)
            css_dict = json.load(open(css_dict_path))[DICT_KEY]

        assert css_dict is not None
        get_css_dict_cache = parse_dict_json(css_dict)
        return get_css_dict_cache

def css_defaults(name, css_dict):
    """Находит первое значение по-умолчанию
    background -> #FFF
    color -> #FFF
    content -> ""
    """
    cur = css_dict.get(name) or css_dict.get(name[1:-1])
    if cur is None:
        return None
    default = cur.get('default')
    if default is not None:
        return default

    for v in cur['values']:
        if v.startswith('<') and v.endswith('>'):
            ret = css_defaults(v, css_dict)
            if ret is not None:
                return ret

def css_flat(name, values=None, css_dict=None):
    """Все значения у свойства (по порядку)
    left -> [u'auto', u'<dimension>', u'<number>', u'<length>', u'.em', u'.ex',
            u'.vw', u'.vh', u'.vmin', u'.vmax', u'.ch', u'.rem', u'.px', u'.cm',
            u'.mm', u'.in', u'.pt', u'.pc', u'<percentage>', u'.%']
    """
    cur = css_dict.get(name) or css_dict.get(name[1:-1])
    if values is None:
        values = []
    if cur is None:
        return values
    for value in cur['values']:
        values.append(value)
        if value.startswith('<') and value.endswith('>'):
            values = css_flat(value, values, css_dict)
    return values

def css_flat_list(name, css_dict):
    """Возвращает список кортежей (свойство, возможное значение)
    left -> [(left, auto), (left, <integer>), (left, .px)...]
    """
    return list(product((name,), css_flat(name, css_dict=get_css_dict())))

def get_flat_css():
    return list(chain.from_iterable(starmap(css_flat_list, ((i, get_css_dict()) for i in get_css_dict()))))
