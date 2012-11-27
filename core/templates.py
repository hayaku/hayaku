# -*- coding: utf-8 -*-
import json
import os
import re

from css_dict_driver import FLAT_CSS
from probe import hayaku_extract, sub_string

CSS_PREFIXES_FILE = 'CSS-dict_prefixes.json'

COLOR_PROPERTY = set(p for p, v in FLAT_CSS if v == '<color_values>')
UNITS_PROPERTY = set(p for p, v in FLAT_CSS if v.startswith('.'))

def align_prefix(property_name, prefix_list, no_unprefixed_property, aligned_prefixes, use_only):
    """Если есть префиксы, сделать шаблон с правильными отступами"""

    # if no_unprefixed_property:
        # prefix_list = ('-{0}-{1}'.format(prefix_list[0], property_name),)

    # skip if `use_only` is empty
    if use_only:
        prefix_list = [p for p in prefix_list if p in use_only]

    if prefix_list:
        prefix_list = ['-{0}-{1}'.format(p, property_name) for p in prefix_list]
        if not no_unprefixed_property:
            prefix_list.append(property_name)
        if not aligned_prefixes:
            return prefix_list
        max_length = max(len(p) for p in prefix_list)
        # TODO: сделать сортировку по размеру значений в prefix_list
        return tuple((' '*(max_length-len(p))) + p for p in prefix_list)
    return (property_name,)

def hex_to_coloralpha(hex):
    if len(hex) == 1:
        hex = hex*2
    return round(float(int(hex, 16)) / 255, 2)

def color_expand(color,alpha):
    if not color:
        return '#'
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
        if color[0] != '#' and alpha == 1:
            alpha = hex_to_coloralpha(color[3])
            color = color[:3]
        else:
            return color
    elif len(color) == 5:
        if color[0] != '#':
            alpha = hex_to_coloralpha(color[3:5])
            color = color[:3]
        else:
            alpha = hex_to_coloralpha(color[4]*2)
            color = color[1:4]
    elif len(color) == 6:
        if color[0] != '#':
            pass
        else:
            alpha = hex_to_coloralpha(color[4:5])
            color = color[1:4]
    elif len(color) == 7:
        color = color[1:]
    else:
        return color

    # Convert color to rgba if there is some alpha
    if alpha == '.' or float(alpha) < 1:
        if alpha == '.':
            alpha = '.${1:5}' # adding caret for entering alpha value
        if alpha == '.0' or alpha == 0:
            alpha = '0'
        if len(color) == 3:
            color = color[0] * 2 + color[1] * 2 + color[2] * 2
        return "rgba({0},{1},{2},{3})".format(int(color[:2],16), int(color[2:4],16), int(color[4:],16), alpha)

    return '#{0}'.format(color)

def length_expand(name, value, unit, options=None):
    if options is None:
        options = {}

    if unit and 'percents'.startswith(unit):
        unit = '%'

    if isinstance(value, float):
        full_unit = options.get('CSS_default_unit_decimal', 'em')
    else:
        full_unit = options.get('CSS_default_unit', 'px')

    if value == 0:
        return '0'
    if value == '':
        return ''

    if unit:
        units = (val[1:] for key, val in FLAT_CSS if key == name and val.startswith('.'))
        req_units = [u for u in units if sub_string(u, unit)]

        PRIORITY = ("em", "ex", "vw", "vh", "vmin", "vmax" "vm", "ch", "rem",
            "px", "cm", "mm", "in", "pt", "pc")
        full_unit = hayaku_extract(unit, req_units, PRIORITY)
        if not full_unit:
            return

    return '{0}{1}'.format(value, full_unit)

def expand_value(args, options=None):
    if 'keyword-value' in args:
        return args['keyword-value']
    if args['property-name'] in COLOR_PROPERTY:
        if 'color' in args and not args['color']:
            return '#'
        return color_expand(args.get('color', ''),args.get('color_alpha', 1))
    elif args['property-name'] in UNITS_PROPERTY and 'keyword-value' not in args:
        ret = length_expand(args['property-name'], args.get('type-value', ''), args.get('type-name', ''), options)
        return ret
    elif 'type-value' in args:
        return str(args['type-value'])
    return args.get('keyword-value', '')

def split_for_snippet(values, offset=0):
    split_lefts = []
    split_rights = []
    new_offset = offset

    for value in (v for v in values if len(v) > 1):
        for i in range(1, len(value)):
            if value[:i] not in split_lefts:
                split_lefts.append(value[:i])
                split_rights.append(value[i:])
                new_offset += 1

    split_lefts = ''.join('({0}$)?'.format(re.escape(i)) for i in split_lefts)
    split_rights = ''.join('(?{0}:{1})'.format(i+1+offset,re.escape(f)) for i,f in enumerate(split_rights))

    return (split_lefts, split_rights, new_offset)

def make_template(args, options):
    whitespace        = options.get('CSS_whitespace_after_colon', '')
    disable_semicolon = options.get('CSS_syntax_no_semicolons', False)
    disable_colon     = options.get('CSS_syntax_no_colons', False)
    disable_prefixes  = options.get('CSS_prefixes_disable', False)

    if not whitespace and disable_colon:
        whitespace = ' '

    value = expand_value(args, options)
    if value is None:
        return

    if value.startswith('[') and value.endswith(']'):
        value = False

    important = args['important'] and ' !important' or ''
    semicolon = ';'
    colon = ':'

    if disable_semicolon:
        semicolon = ''
    if disable_colon:
        colon = ''

    property_ = (args['property-name'],)
    if not disable_prefixes:
        property_ = align_prefix(
            args['property-name'],
            args.get('prefixes', []),
            args.get('no-unprefixed-property', False) or options.get('CSS_prefixes_no_unprefixed', False),
            options.get('CSS_prefixes_align', True),
            options.get('CSS_prefixes_only', []),
            )

    # Replace the parens with a tabstop snippet
    # TODO: Move the inside snippets to the corresponding snippets dict
    if value and '()' in value:
        if value.replace('()', '') in ['rotate','rotateX','rotateY','rotateZ','skew','skewX','skewY']:
            value = value.replace('()', '($1${1/^((?!0$)-?(\d*.)?\d+)?.*$/(?1:deg)/m})')
        else:
            value = value.replace('()', '($1)')

    default_placeholder = '$1'
    if 'default-value' in args:
        default_placeholder = ''.join([
            '${1:',
            args['default-value'],
            '}',
            ])
    if not value or value == "#":
        if not options.get('CSS_disable_postexpand', False):
            auto_values = [val for prop, val in FLAT_CSS if prop == args['property-name']]
            if auto_values:
                units = []
                values = []

                if disable_semicolon:
                    semicolon = ' ' # Not empty, 'cause then the switching between tabstops in postexpand wouldn't work

                for p_value in (v for v in auto_values if len(v) > 1):
                    if p_value.startswith('.'):
                        units.append(p_value[1:])
                    elif not p_value.startswith('<'):
                        values.append(p_value)


                values_splitted = split_for_snippet(values)
                snippet_values = ''.join([
                    '${1/^',
                    values_splitted[0],
                    '.*/',
                    values_splitted[1],
                    '/m}',
                    ])

                snippet_units = ''
                if units:
                    units_splitted = split_for_snippet(units, 4)
                    snippet_units = ''.join([
                        '${1/((?!^0$)(?=.)[\d\-]*(\.)?(\d+)?((?=.)',
                        units_splitted[0],
                        ')?$)?.*/(?4:',
                        units_splitted[1],
                        ':(?1:(?2:(?3::0)em:px)))/m}',
                        ])

                # Special case for colors
                if value == "#":
                    value = ''.join([
                        '${1/^(?=((\d{1,3}%?),(\.)?(.+)?$)?).+$/(?1:rgba\((?3:$2,$2,))/m}',            # Rgba start
                        '${1/^(?=(\((.+)?$)?).+$/(?1:rgba)/m}',                                        # Alternate rgba start
                        '${1/^(?=([0-9a-fA-F]{1,6}$)?).+$/(?1:#)/m}',                                  # If in need of hash
                        default_placeholder,
                        '${1/^(#?([0-9a-fA-F]{1,2})$)?.*/(?1:(?2:$2$2))/m}',                           # Hex Digit multiplication
                        '${1/^(?=((\d{1,3}%?),(\.)?(.+)?$)?).+$/(?1:(?3:(?4::5):(?4::$2,$2,1))\))/m}', # Rgba end
                        snippet_values,
                        ])
                        # TODO: add hsla (look at percents?)
                        # TODO: remove hash from the default value to ease the writing of the numbers
                else:
                    value = default_placeholder + snippet_values + snippet_units
        else:
            value = default_placeholder
    value = value or ''

    return '\n'.join(''.join([
        '{0}',
        colon,
        whitespace,
        '{1}',
        important,
        semicolon,
        ]).format(prop, value) for prop in property_)

# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
