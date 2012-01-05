# -*- coding: utf-8 -*-

CSS_DICT_FILENAME = 'CSS-dict.txt'

# парсер формата файла с css-правилами

class CssRule(object):
    def __init__(self, name):
        self.name = name

def read_file(filename):
    with open(filename) as file_dict:
        for line in file_dict:
            line = line.strip()
            # skip comments
            if line.lstrip().startswith('#'):
                continue
            # added extra markup
            if not line:
                line = ':'
            # strip comment at the end line
            if '#' in line:
                sharp_index = line.find('#')
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
    return css

if __name__ == '__main__':
    print parse_dict(read_file(CSS_DICT_FILENAME))