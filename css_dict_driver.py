# -*- coding: utf-8 -*-

from itertools import product

# CSS_DICT_FILENAME = 'core/CSS-dict.txt'
CSS_DICT_FILENAME = 'CSS-dict.txt'

# парсер формата файла с css-правилами

COMMENT = '//'

def read_file(filename):
    with open(filename) as file_dict:
        for line in file_dict:
            line = line.strip()
            # skip comments
            if line.lstrip().startswith(COMMENT):
                continue
            # added extra markup
            if not line:
                line = ':'
            # strip comment at the end line
            if COMMENT in line:
                sharp_index = line.find(COMMENT)
                line = line[:sharp_index]
            yield line

def parse_dict(lines):
    tokenize = ' '.join(lines).split(':')
    cleanup = [line.strip() for line in tokenize if line.strip()]
    properties = (tuple(p.strip() for p in prop.split(',')) for prop in cleanup[::2])
    values = (tuple(v.strip() for v in value.split('|')) for value in cleanup[1::2])
    parsed = zip(properties, values)
    del cleanup, properties, values, tokenize, lines

    css = []
    for properties, values in parsed:
        for p in properties:
            for v in values:
                css.append((p, v))
    parsed_dict = {}
    for k, v in css:
        parsed_dict.setdefault(k, set()) # заменить на defaultdict?
        parsed_dict[k].add(v)
    return parsed_dict

def expand_values(parsed_dict, properties):
    if not properties:
        return parsed_dict
    prop = properties.pop()
    prop_find = '<{0}>'.format(prop)
    for name, values in parsed_dict.items():
        # todo: пересмотреть алгоритм
        if prop_find in values:
            values.remove(prop_find)
            values |= parsed_dict[prop]
        if prop in values:
            values.remove(prop)
            values |= set(p for p in parsed_dict[prop])
    return expand_values(parsed_dict, properties)

def flat_dict(dict_):
    arr = []
    for k, v in dict_.items():
        arr.extend(product((k,), v))
    return arr

def props_dict():
    pd = parse_dict(read_file(CSS_DICT_FILENAME))
    new_dict = {}
    for k, val in pd.items():
        v = (i for i in val if '<' not in i and not i.startswith('.'))
        new_dict[k] = (list(v),)
    return new_dict

def flat_css_dict():
    """Возвращает список (свойство, возможное_значение)"""
    pd = parse_dict(read_file(CSS_DICT_FILENAME))
    all_pd = expand_values(pd, pd.keys())
    return flat_dict(all_pd)

if __name__ == '__main__':
    pd = parse_dict(read_file(CSS_DICT_FILENAME))
    all_pd = expand_values(pd, pd.keys())
    for p, v in flat_dict(all_pd):
        if v in ('<number>', '<attr>') or p == 'top':
            print p, v
