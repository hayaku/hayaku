# -*- coding: utf-8 -*-
import re

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
COLOR_PROPERTY = set([
    'outline-color',
    'border-color',
    'border-top-color',
    'border-right-color',
    'border-bottom-color',
    'border-left-color',
    'background-color',
    'color',
    'text-emphasis-color',
])

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
    if len(color) == 7:
        return color.upper()
    elif len(color) in (1, 2):
        pass
    elif len(color) == 3 and color[0] == '#':
        color = color[1:]
    else:
        return ''
    return '#{0}'.format(color * 3).upper()

def length_expand(value):
    # print value
    m = re.search(r'([a-z%]+)$', value)
    # print m
    if m is not None:
        UNITS = {'p': 'px', 'pe': '%', 'e': 'em'}
        pre_unit = m.group(1)
        unit = UNITS.get(pre_unit, pre_unit)
        # print unit, 'unit', pre_unit
        value = value[:-len(pre_unit)]
    else:
        if value:
            unit = 'px'
        else:
            unit = ''
    if '.' in value:
        unit = 'em'
    # print value, 'value'
    return '{0}{1}'.format(value, unit)

def make_template(property_, value='', is_num=False, important=False):
    if property_ in COLOR_PROPERTY:
        value = color_expand(value)
    else:
        value = length_expand(value)
    # print value, property_
    property_ = align_prefix(property_)
    if not value:
        raw = '{0}: ${{1}};${{0}}'
        if important:
            raw = '{0}: ${{1}} !important;${{0}}'
        # print raw, 'raw'
        template_i = (raw.format(prop) for prop in property_)
    else:
        raw = '{0}: {1};${{0}}'
        if important:
            raw = '{0}: {1} !important;${{0}}'
            # raw = '{0}: {1} ;${{0}}'
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
