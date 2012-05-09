# -*- coding: utf-8 -*-
import json
import re

from css_dict_driver import flat_css_dict


CSS_PREFIXES_FILE = 'CSS-dict_prefixes.json'
VENDOR_PROPERTY_PREFIXES = json.loads(open(CSS_PREFIXES_FILE).read())

ALL_CSS_DICT = flat_css_dict()
COLOR_PROPERTY = set(p for p, v in ALL_CSS_DICT if v == '<color>')
UNITS_PROPERTY = set(p for p, v in ALL_CSS_DICT if v.startswith('.'))

def align_prefix(prefix):
    """Если есть префиксы, сделать шаблон с правильными отступами"""
    prefix_list = VENDOR_PROPERTY_PREFIXES.get(prefix, [])
    if prefix_list:
        prefix_list = ['-{0}-{1}'.format(p, prefix) for p in prefix_list]
        prefix_list.append(prefix)
        # TODO: считать max_length при инициализации VENDOR_PROPERTY_PREFIXES
        max_length = max(len(p) for p in prefix_list)
        # TODO: сделать сортировку по размеру значений в prefix_list
        return tuple((' '*(max_length-len(p))) + p for p in prefix_list)
    return (prefix,)

def color_expand(color):
    color = color.upper()
    if len(color) == 1:
        if color == '#':
            color = ''
        else:
            color = color * 3
    elif len(color) == 2:
        if color[0] == '#':
            color = color[1] * 3
        else:
            color = color * 3
    elif len(color) == 3:
        if color[0] == '#':
            color = color[1:] * 3
        else:
            color = color
    elif len(color) == 4:
        if color[0] == '#':
            color = color[1:]
        else:
            return color
    elif len(color) == 6:
        pass
    elif len(color) == 7:
        return color
    else:
        return color
    return '#{0}'.format(color)

def length_expand(value):
    m = re.search(r'([a-z%]+)$', value)
    if m is not None:
        UNITS = {'p': 'px', 'pe': '%', 'e': 'em'}
        pre_unit = m.group(1)
        unit = UNITS.get(pre_unit, pre_unit)
        value = value[:-len(pre_unit)]
    else:
        if value:
            unit = 'px'
        else:
            unit = ''
    if '.' in value:
        unit = 'em'
    try:
        # if value is 0
        if not int(value):
            unit = ''
    except ValueError:
        pass
    return '{0}{1}'.format(value, unit)

def expand_value(property_, value):
    if property_ in COLOR_PROPERTY:
        return color_expand(value)
    elif property_ in UNITS_PROPERTY:
        return length_expand(value)
    return value

def make_template(whitespace, property_, value='', is_num=False, important=False):
    value = expand_value(property_, value)

    property_ = align_prefix(property_)
    if not value:
        raw = '{0}:' + whitespace + '${{1}};${{0}}'
        if important:
            raw = '{0}:' + whitespace + '${{1}} !important;${{0}}'
        # print raw, 'raw'
        template_i = (raw.format(prop) for prop in property_)
    else:
        if value == '#':
            raw = '{0}:' + whitespace + '{1}${{1}};'
        else:
            raw = '{0}:' + whitespace + '{1};${{0}}'
        if important:
            raw = '{0}:' + whitespace + '{1} !important;${{0}}'
            # raw = '{0}: {1} ;${{0}}'
        # print value, 'value'
        # print raw, 'raw'
        template_i = (raw.format(prop, value) for prop in property_)
    return '\n'.join(template_i)

if __name__ == '__main__':
    print make_template('box-shadow', '', False, True)

# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
