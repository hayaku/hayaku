# -*- coding: utf-8 -*-
import json
import os
import re

import sublime

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)


try:
    get_flat_css = import_dir('css_dict_driver', ('get_flat_css',)).get_flat_css
except ImportError:
    from css_dict_driver import get_flat_css

try:
    imp = import_dir('probe', ('hayaku_extract', 'sub_string'))
    hayaku_extract, sub_string = imp.hayaku_extract, imp.sub_string
except ImportError:
    from probe import hayaku_extract, sub_string


COLOR_REGEX = re.compile(r'#([0-9a-fA-F]{3,6})')
COMPLEX_COLOR_REGEX = re.compile(r'^\s*(#?([a-fA-F\d]{3}|[a-fA-F\d]{6})|(rgb|hsl)a?\([^\)]+\))\s*$')
IMAGE_REGEX = re.compile(r'^\s*([^\s]+\.(jpg|jpeg|gif|png))\s*$')

CAPTURING_GROUPS = re.compile(r'(?<!\\)\((?!\?[^<])')
CAPTURES = re.compile(r'(\(\?|\$)(\d+)|^(\d)')

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

    if '<number>' in [val for prop, val in get_flat_css() if prop == name] and not options.get('CSS_units_for_unitless_numbers'):
        full_unit = ''

    if value == 0:
        return '0'
    if value == '':
        return ''

    if unit:
        units = (val[1:] for key, val in get_flat_css() if key == name and val.startswith('.'))
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
    if args['property-name'] in set(p for p, v in get_flat_css() if v == '<color_values>'):
        if 'color' in args and not args['color']:
            return '#'
        return color_expand(args.get('color', ''),args.get('color_alpha', 1))
    elif args['property-name'] in set(p for p, v in get_flat_css() if v.startswith('.')) and 'keyword-value' not in args:
        ret = length_expand(args['property-name'], args.get('type-value', ''), args.get('type-name', ''), options)
        return ret
    elif 'type-value' in args:
        return str(args['type-value'])
    return args.get('keyword-value', '')

def split_for_snippet(values, offset=0):
    split_lefts = [[]]
    split_rights = [[]]
    parts = 0
    new_offset = offset

    for value in (v for v in values if len(v) > 1):
        for i in range(1, len(value)):
            if value[:i] not in [item for sublist in split_lefts for item in sublist] + values:
                if len(split_lefts[parts]) > 98:
                    parts += 1
                    split_lefts.append([])
                    split_rights.append([])
                split_lefts[parts].append(value[:i])
                split_rights[parts].append(value[i:])
                new_offset += 1

    for index in range(0, parts + 1):
        split_lefts[index] = ''.join('({0}$)?'.format(re.escape(i)) for i in split_lefts[index])
        split_rights[index] = ''.join('(?{0}:{1})'.format(i+1+offset,re.escape(f)) for i,f in enumerate(split_rights[index]))

    return (split_lefts, split_rights, new_offset)

def convert_to_parts(parts):
    matches = []
    inserts = []
    parts_count = 1

    # Function for offsetting the captured groups in inserts
    def offset_captures(match):
        if match.group(3):
            return '()' + match.group(3)
        else:
            number = int(match.group(2))
            return match.group(1) + str(number + parts_count)

    for part in parts:
        matches.append(''.join([
            '(?=(',
            part['match'],
            ')?)',
            ]))
        inserts.append(''.join([
            '(?',
            str(parts_count),
            ':',
            CAPTURES.sub(offset_captures, part['insert']),
            ')',
            ]))
        # Incrementing the counter, adding the number of internal capturing groups
        parts_count += 1 + len(CAPTURING_GROUPS.findall(part['match'] ))
    return { "matches": matches, "inserts": inserts }

def generate_snippet(data):
    value = data.get('value')
    before = ''.join([
        '_PROPERTY_',
        data.get('colon'),
        data.get('space'),
        ])
    after = ''
    importance = ''
    if data.get('important'):
        importance = ' !important'

    if value:
        after = importance + data.get('semicolon')
    else:
        if not importance:
            importance_splitted = split_for_snippet(["!important"])
            importance = ''.join([
                '${1/.*?',
                importance_splitted[0][0],
                '$/',
                importance_splitted[1][0],
                '/}',
                ])

        befores = convert_to_parts(data["before"])
        before = ''.join([
            '${1/^',
            ''.join(befores["matches"]),
            '.+$|.*/',
            before,
            ''.join(befores["inserts"]),
            '/m}',
            ])


        if data.get('semicolon') == '':
            data['semicolon'] = ' '

        afters = convert_to_parts(data["after"])
        after = ''.join([
            '${1/^',
            ''.join(afters["matches"]),
            '.+$|.*/',
            ''.join(afters["inserts"]),
            '/m}',
            data.get('autovalues'),
            importance,
            data.get('semicolon'),
            ])
        value = ''.join([
            '${1:',
            data.get('default'),
            '}',
            ])
    return (before + value + after).replace('{','{{').replace('}','}}').replace('_PROPERTY_','{0}')


def make_template(args, options):
    whitespace        = options.get('CSS_whitespace_after_colon', '')
    disable_semicolon = options.get('CSS_syntax_no_semicolons', False)
    disable_colon     = options.get('CSS_syntax_no_colons', False)
    disable_prefixes  = options.get('CSS_prefixes_disable', False)
    clipboard = sublime.get_clipboard()

    if not whitespace and disable_colon:
        whitespace = ' '

    value = expand_value(args, options)
    if value is None:
        return

    if value.startswith('[') and value.endswith(']'):
        value = False

    semicolon = ';'
    colon = ':'

    if disable_semicolon:
        semicolon = ''
    if disable_colon:
        colon = ''

    snippet_parts = {
        'colon': colon,
        'semicolon': semicolon,
        'space': whitespace,
        'default': args.get('default-value',''),
        'important': args.get('important'),
        'before': [],
        'after': [],
        'autovalues': '',
    }

    # Handling prefixes
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

    # Do things when there is no value expanded
    if not value or value == "#":
        if not options.get('CSS_disable_postexpand', False):
            auto_values = [val for prop, val in get_flat_css() if prop == args['property-name']]
            if auto_values:
                units = []
                values = []

                for p_value in (v for v in auto_values if len(v) > 1):
                    if p_value.startswith('.'):
                        units.append(p_value[1:])
                    elif not p_value.startswith('<'):
                        values.append(p_value)

                values_splitted = split_for_snippet(values)
                snippet_values = ''
                for index in range(0,len(values_splitted[0])):
                    snippet_values += ''.join([
                        '${1/^\s*',
                        values_splitted[0][index],
                        '.*/',
                        values_splitted[1][index],
                        '/m}',
                        ])
                snippet_parts['autovalues'] += snippet_values

                snippet_units = ''
                # TODO: find out when to use units or colors
                # TODO: Rewrite using after
                if units and value != "#":
                    units_splitted = split_for_snippet(units, 4)
                    snippet_parts['before'].append({
                        "match":  "%$",
                        "insert": "100"
                        })
                    # If there can be `number` in value, don't add `em` automatically
                    optional_unit_for_snippet = '(?2:(?3::0)em:px)'
                    if '<number>' in auto_values and not options.get('CSS_units_for_unitless_numbers'):
                        optional_unit_for_snippet = '(?2:(?3::0):)'
                    snippet_units = ''.join([
                        '${1/^\s*((?!0$)(?=.)[\d\-]*(\.)?(\d+)?((?=.)',
                        units_splitted[0][0],
                        ')?$)?.*/(?4:',
                        units_splitted[1][0],
                        ':(?1:' + optional_unit_for_snippet + '))/m}',
                        ])
                    snippet_parts['autovalues'] += snippet_units

                # Adding snippets for colors
                if value == "#":
                    value = ''
                    # Insert hash and doubling letters
                    snippet_parts['before'].append({
                        "match":  "([0-9a-fA-F]{1,6}|[0-9a-fA-F]{3,6}\s*(!\w*\s*)?)$",
                        "insert": "#"
                        })
                    snippet_parts['after'].append({
                        "match": "#?([0-9a-fA-F]{1,2})$",
                        "insert": "(?1:$1$1)"
                        })
                    # Insert `rgba` thingies
                    snippet_parts['before'].append({
                        "match":  "(\d{1,3}%?),(\.)?.*$",
                        "insert": "rgba\((?2:$1,$1,)"
                        })
                    snippet_parts['after'].append({
                        "match": "(\d{1,3}%?),(\.)?(.+)?$",
                        "insert": "(?2:(?3::5):(?3::$1,$1,1))\)"
                        })

                    # Getting the value from the clipboard
                    # TODO: Move to the whole clipboard2default function
                    check_clipboard_for_color = COMPLEX_COLOR_REGEX.match(clipboard)
                    if check_clipboard_for_color and 'colors' in options.get('CSS_clipboard_defaults'):
                        snippet_parts['default'] = check_clipboard_for_color.group(1)
                # TODO: move this out of `if not value`,
                #       so we could use it for found `url()` values
                if '<url>' in auto_values:
                    snippet_parts['before'].append({
                        "match":  "[^\s]+\.(jpg|jpeg|gif|png)$",
                        "insert": "url\("
                        })
                    snippet_parts['after'].append({
                        "match": "[^\s]+\.(jpg|jpeg|gif|png)$",
                        "insert": "\)"
                        })
                    check_clipboard_for_image = IMAGE_REGEX.match(clipboard)
                    if check_clipboard_for_image and 'images' in options.get('CSS_clipboard_defaults'):
                        quote_symbol = ''
                        if options.get('CSS_syntax_url_quotes'):
                            quote_symbol = options.get('CSS_syntax_quote_symbol')
                        snippet_parts['default'] = 'url(' + quote_symbol + check_clipboard_for_image.group(1) + quote_symbol + ')'


    snippet_parts['value'] = value or ''

    snippet = generate_snippet(snippet_parts)

    # Apply settings to the colors in the values
    def restyle_colors(match):
        color = match.group(1)
        # Change case of the colors in the value
        if options.get('CSS_colors_case').lower() in ('uppercase' 'upper'):
            color = color.upper()
        elif options.get('CSS_colors_case').lower() in ('lowercase' 'lower'):
            color = color.lower()
        # Make colors short or longhand
        if options.get('CSS_colors_length').lower() in ('short' 'shorthand') and len(color) == 6:
            if color[0] == color[1] and color[2] == color[3] and color[4] == color[5]:
                color = color[0] + color[2] + color[4]
        elif options.get('CSS_colors_length').lower() in ('long' 'longhand') and len(color) == 3:
            color = color[0] * 2 + color[1] * 2 + color[2] * 2
        return '#' + color
    snippet = COLOR_REGEX.sub(restyle_colors, snippet)

    # Apply setting of the prefered quote symbol

    if options.get('CSS_syntax_quote_symbol') == "'" and '"' in snippet:
        snippet = snippet.replace('"',"'")
    if options.get('CSS_syntax_quote_symbol') == '"' and "'" in snippet:
        snippet = snippet.replace("'",'"')

    newline_ending = ''
    if options.get('CSS_newline_after_expand'):
        newline_ending = '\n'
    return '\n'.join(snippet.format(prop) for prop in property_) + newline_ending

# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
