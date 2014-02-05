# -*- coding: utf-8 -*-
import os
import re

import sublime
import sublime_plugin

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)

try:
    get_values_by_property = import_dir('hayaku_dict_driver', ('get_values_by_property',)).get_values_by_property
except ImportError:
    from hayaku_dict_driver import get_values_by_property

try:
    get_key_from_property = import_dir('hayaku_dict_driver', ('get_key_from_property',)).get_key_from_property
except ImportError:
    from hayaku_dict_driver import get_key_from_property

class HayakuCyclingThroughValuesCommand(sublime_plugin.TextCommand):
    def run(self, edit, modifier = 1):
        self.edit = edit

        # Set the modifier from the direction and amount
        self.modifier = modifier

        self.dirty_regions = []
        for index, region in enumerate(self.view.sel()):
            self.region = region
            self.region_index = index
            self.new_value = None
            self.current_value = {}

            # Check if the current region was in the area where the first one made changes to
            should_proceed = not any(dirty_region.intersects(region) for dirty_region in self.dirty_regions)

            # Check if the region is multiline
            if self.view.line(self.region) != self.view.line(self.region.begin()):
                should_proceed = False

            if should_proceed:
                self.get_current_CSS_value()
                self.get_current_numeric_value()
                self.rotate_CSS_string()
                self.rotate_numeric_value()
                self.apply_current_value()

    def get_new_position(self, initial_position, detected_region, new_value):
        def adjust_offset(adjusted_offset):
            offset = len(new_value) - len(self.view.substr(detected_region))

            if adjusted_offset >= detected_region.end():
                adjusted_offset = adjusted_offset + offset
            elif adjusted_offset in range(detected_region.begin() + 1, detected_region.end()):
                adjusted_offset = adjusted_offset + offset
                if adjusted_offset < detected_region.begin():
                    adjusted_offset = detected_region.begin()
            return adjusted_offset

        return sublime.Region(
            adjust_offset(initial_position.begin()),
            adjust_offset(initial_position.end()))

    def apply_current_value(self):
        if not self.new_value:
            return False

        old_position = self.view.sel()[self.region_index]
        new_position = self.get_new_position(old_position, self.current_value.get('region'), self.new_value)

        if old_position != new_position:
            self.view.sel().subtract(old_position)

        self.view.replace(self.edit, self.current_value.get('region'), self.new_value)
        self.dirty_regions.append(self.current_value.get('region'))

        if old_position != new_position:
            self.view.sel().add(new_position)

    def get_closest_value(self, input, input_index, splitter, guard = None):
        if not input:
            return False, False
        result = None
        result_index = None

        prev_item = None
        prev_item_begin = None
        prev_item_end = input_index
        for index, item in enumerate(re.finditer(splitter, input)):
            current_item = item.group(1)
            current_item_begin = input_index + item.start(1)
            left_boundary = current_item_begin - (current_item_begin - prev_item_end + 1) // 2
            right_boundary = input_index + item.end(1) + 1

            if not (guard and re.match(guard, current_item)):
                if not result:
                    result = current_item
                    result_index = current_item_begin

                if self.region.begin() in range(input_index, result_index + len(result)):
                    break
                if self.region.begin() in range(prev_item_end, left_boundary):
                    result = prev_item
                    result_index = prev_item_begin
                    break
                elif index > 0 and self.region.begin() >= left_boundary:
                    result = current_item
                    result_index = current_item_begin

            prev_item = current_item
            prev_item_begin = current_item_begin
            prev_item_end = right_boundary
        return result, result_index

    def get_current_CSS_value(self):
        if self.current_value.get('value') or not sublime.score_selector(self.view.scope_name(self.region.a), 'source.css, source.less, source.sass, source.scss, source.stylus'):
            return False

        # TODO: think on the get_closest_value to accept Region
        declaration, declaration_index = self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'([^;]+;?)',
            r'^\s*\/\*|^\W+$'
            )

        if not declaration:
            return False

        # Parsed declaration                    prefix        property       delimiter    values
        parsed_declaration = re.search(r'^(\s*)(-[a-zA-Z]+-)?([a-zA-Z0-9-]+)(\s*(?: |\:))((?:(?!\!important).)+)', declaration)
        if not parsed_declaration:
            return False
        declaration_index = declaration_index + parsed_declaration.start(5)

        # TODO: make the get_closest_value to return Region
        value, value_index = self.get_closest_value(
            parsed_declaration.group(5),
            declaration_index,
            r'(#[a-zA-Z0-9]{3,6}|((?<![\w])-)?[0-9]*((?<![\.])\.)?[0-9]+[a-zA-Z%]*|[a-zA-Z\-]+)'
            )

        if value:
            self.current_value['context'] = 'CSS value'
            self.current_value['value'] = value
            self.current_value['region'] = sublime.Region(value_index, value_index + len(value))
            self.current_value['prop'] = parsed_declaration.group(3)

    def get_current_numeric_value(self):
        if self.current_value.get('value'):
            return False

        # TODO: make the get_closest_value to return Region
        word_like, word_like_index = self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'(\S+)',
            r'(^[^0-9]+$)',
            )
        # TODO: make the get_closest_value to return Region
        number, number_index = self.get_closest_value(
            word_like,
            word_like_index,
            r'(((?<![\w])-)?[0-9]*((?<![\.])\.)?[0-9]+)'
            )

        if number:
            self.current_value['context'] = 'Number'
            self.current_value['value'] = number
            self.current_value['region'] = sublime.Region(number_index, number_index + len(number))


    def rotate_CSS_string(self):
        if self.new_value or not (self.current_value.get('value') and self.current_value.get('prop')):
            return False

        props_values = get_values_by_property(self.current_value.get('prop'))
        if self.current_value.get('value') in props_values:
            index = props_values.index(self.current_value.get('value'))
            if self.modifier > 0:
                index += 1
            elif self.modifier < 0:
                index -= 1
            # else we should edit it
            self.new_value = props_values[index % len(props_values)]

    def rotate_numeric_value(self):
        if self.new_value or not self.current_value.get('value'):
            return False

        left_limit = float("-inf")
        if self.current_value.get('prop'):
            if get_key_from_property(self.current_value.get('prop'), 'always_positive'):
                left_limit = float(0)

        found_number = re.search(r'^(-?\d*\.?\d+)(.*)$', self.current_value.get('value'))
        if found_number:
            new_value = max(left_limit, round(float(found_number.group(1)) + self.modifier, 13))

            # Check if we need to add mandatory unit
            # replace with postexpand in the future?
            postfix = ''
            if found_number.group(1) == '0' and found_number.group(2) == '' and self.current_value.get('context') == 'CSS value':
                possible_values = get_key_from_property(self.current_value.get('prop'), 'values')
                if '<dimension>' in possible_values or '<length>' in possible_values:
                    if new_value % 1 == 0:
                        postfix = 'px'
                    else:
                        postfix = 'em'

            self.new_value = str(new_value).rstrip('0').rstrip('.') + postfix + found_number.group(2)
