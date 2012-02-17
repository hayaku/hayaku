# -*- coding: utf-8 -*-
import re

from css_dict_driver import flat_css_dict

# TODO заменить на css-dict
VENDOR_PROPERTY_PREFIXES = {
    'box-shadow': (
        '-webkit-box-shadow',
        '-moz-box-shadow',
        '-o-box-shadow',
        'box-shadow',
    ),
    'box-sizing': (
        '-webkit-box-sizing',
        '-moz-box-sizing',
        'box-sizing',
    ),
    'border-radius': (
        '-webkit-border-radius',
        '-moz-border-radius',
        'border-radius',
    ),
    'user-select': (
        '-webkit-user-select',
        '-moz-user-select',
        'user-select',
    ),
    'transform': (
        '-webkit-transform',
        '-moz-transform',
        '-o-transform',
        'transform',
    ),
    'background-clip': (
        '-webkit-background-clip',
        '-moz-background-clip',
        'background-clip',
    ),
    'border-top-right-radius': (
        '-webkit-border-top-right-radius',
        '-moz-border-radius-topright',
        '-o-border-top-right-radius',
        'border-top-right-radius',
    ),
    'border-top-left-radius': (
        '-webkit-border-top-left-radius',
        '-moz-border-radius-topleft',
        '-o-border-top-left-radius',
        'border-top-left-radius',
    ),
    'border-bottom-right-radius': (
        '-webkit-border-bottom-right-radius',
        '-moz-border-radius-bottomright',
        '-o-border-bottom-right-radius',
        'border-bottom-right-radius',
    ),
    'border-bottom-left-radius': (
        '-webkit-border-bottom-left-radius',
        '-moz-border-radius-bottomleft',
        '-o-border-bottom-left-radius',
        'border-bottom-left-radius',
    ),
}

ALL_CSS_DICT = flat_css_dict()
COLOR_PROPERTY = set(p for p, v in ALL_CSS_DICT if v == '<color>')
UNITS_PROPERTY = set(p for p, v in ALL_CSS_DICT if v.startswith('.'))

def align_prefix(prefix):
    """Если есть префиксы, сделать шаблон с правильными отступами"""
    prefix_list = VENDOR_PROPERTY_PREFIXES.get(prefix, [])
    if prefix_list:
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

def make_template(property_, value='', is_num=False, important=False, whitespace=' '):
    value = expand_value(property_, value)

    property_ = align_prefix(property_)
    car_template = '{0}:' + whitespace
    if not value:
        raw = car_template + '${{1}};${{0}}'
        if important:
            raw = car_template + '${{1}} !important;${{0}}'
        # print raw, 'raw'
        template_i = (raw.format(prop) for prop in property_)
    else:
        if value == '#':
            raw = car_template + '{1}${{1}};'
        else:
            raw = car_template + '{1};${{0}}'
        if important:
            raw = car_template + '{1} !important;${{0}}'
            # raw = '{0}: {1} ;${{0}}'
        # print value, 'value'
        # print raw, 'raw'
        template_i = (raw.format(prop, value) for prop in property_)
    return '\n'.join(template_i)

if __name__ == '__main__':
    print make_template('box-shadow', '', False, True)
    print make_template('zoom', '1', False, False)
    print make_template('width', '1', False, False)

# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
