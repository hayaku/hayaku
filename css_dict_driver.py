# -*- coding: utf-8 -*-
# (c) 2012 Sergey Mezentsev
import json
import string
import os

from itertools import chain, product

JSON_CSS_DICT_FILENAME =  os.path.join('dictionaries', 'CSS-dict.json')

# парсер формата файла с css-правилами

def file_path(filename):
    filepath = os.path.join('.', filename)
    return filepath if os.path.exists(filepath) else os.path.join('.', 'core', filename)

def parse_dict_json(raw_dict):
    result_dict = {}

    valuable = (i for i in raw_dict if 'name' in i and 'values' in i)

    for i in valuable:
        name, values, default = i['name'], i['values'], i.get('default')
        names = name if isinstance(name, list) else map(string.strip, name.split(','))
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

CSS_DICT = parse_dict_json(json.load(open(file_path(JSON_CSS_DICT_FILENAME))))

def css_defaults(name):
    """Находит первое значение по-умолчанию
    background -> #FFF
    color -> #FFF
    content -> ""
    """
    cur = CSS_DICT.get(name) or CSS_DICT.get(name[1:-1])
    if cur is None:
        return None
    default = cur.get('default')
    if default is not None:
        return default

    for v in cur['values']:
        if v.startswith('<') and v.endswith('>'):
            ret = css_defaults(v)
            if ret is not None:
                return ret

def css_flat(name, values=None):
    """Все значения у свойства (по порядку)
    left -> [u'auto', u'<dimension>', u'<number>', u'<length>', u'.em', u'.ex',
            u'.vw', u'.vh', u'.vmin', u'.vmax', u'.ch', u'.rem', u'.px', u'.cm',
            u'.mm', u'.in', u'.pt', u'.pc', u'<percentage>', u'.%']
    """
    cur = CSS_DICT.get(name) or CSS_DICT.get(name[1:-1])
    if values is None:
        values = []
    if cur is None:
        return values
    for value in cur['values']:
        values.append(value)
        if value.startswith('<') and value.endswith('>'):
            values = css_flat(value, values)
    return values

def css_flat_list(name):
    """Возвращает список кортежей (свойство, возможное значение)
    left -> [(left, auto), (left, <integer>), (left, .px)...]
    """
    return list(product((name,), css_flat(name)))

FLAT_CSS = list(chain.from_iterable(map(css_flat_list, CSS_DICT)))
