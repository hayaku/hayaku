# -*- coding: utf-8 -*-
import json
import os
import re

from css_dict_driver import flat_css_dict
from probe import hayaku_extract, sub_string

CSS_PREFIXES_FILE = 'CSS-dict_prefixes.json'
VENDOR_PROPERTY_PREFIXES = json.loads(open(
    os.path.join('core', CSS_PREFIXES_FILE) if not os.path.exists(CSS_PREFIXES_FILE) else CSS_PREFIXES_FILE
).read())

ALL_CSS_DICT = flat_css_dict()
COLOR_PROPERTY = set(p for p, v in ALL_CSS_DICT if v == '<color>')
UNITS_PROPERTY = set(p for p, v in ALL_CSS_DICT if v.startswith('.'))

def align_prefix(prefix, need_prefixes=True):
    """Если есть префиксы, сделать шаблон с правильными отступами"""
    prefix_list = VENDOR_PROPERTY_PREFIXES.get(prefix, [])
    if prefix_list and need_prefixes:
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

def length_expand(name, value, unit):
    # TODO: добавить тесты к функции
    full_unit = 'em' if isinstance(value, float) else 'px'
    if unit:
        units = (val[1:] for key, val in ALL_CSS_DICT if key == name and val.startswith('.'))
        req_units = [u for u in units if sub_string(u, unit)]

        PRIORITY = ('px', 'em')
        full_unit = hayaku_extract(unit, req_units, PRIORITY)

    return '{0}{1}'.format(value, full_unit)

def expand_value(args):
    if args['property-name'] in COLOR_PROPERTY:
        return color_expand(args.get('color', ''))
    elif args['property-name'] in UNITS_PROPERTY:
        return length_expand(args['property-name'], args.get('type-value', ''), args.get('type-name', ''))
    return args.get('keyword-value', '')

def make_template(args, options):
    whitespace = options['whitespace'] or ' '
    disable_semicolon = options['disable_semicolon'] or False
    disable_colon = options['disable_colon'] or False
    disable_prefixes = options['disable_prefixes'] or False
    
    value = expand_value(args)
    important = args['important']
    semicolon = ';'
    colon = ':'

    if disable_semicolon:
        semicolon = ''
    if disable_colon:
        colon = ''

    property_ = align_prefix(args['property-name'], not disable_prefixes)

    value_container = '${{{{1:{0}}}}}'.format(args['default-value']) if 'default-value' in args else '${{1}}'

    if not value:
        raw = '{0}' + colon + whitespace + value_container + semicolon + '${{0}}'
        if important:
            raw = '{0}' + colon + whitespace + value_container +' !important' + semicolon + '${{0}}'
        template_i = (raw.format(prop) for prop in property_)
    else:
        if value == '#':
            raw = '{0}' + colon + whitespace + '{1}${{1}}' + semicolon
        else:
            raw = '{0}' + colon + whitespace + '{1}' + semicolon + '${{0}}'
        if important:
            raw = '{0}' + colon + whitespace + '{1} !important' + semicolon + '${{0}}'
            # raw = '{0}: {1} ;${{0}}'
        # print value, 'value'
        # print raw, 'raw'
        template_i = (raw.format(prop, value) for prop in property_)
    return '\n'.join(template_i)

# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
