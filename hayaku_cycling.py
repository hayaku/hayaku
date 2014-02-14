# -*- coding: utf-8 -*-
import os
import re
import math
import datetime

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
                self.get_current_date()
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

        all_founds = []

        for index, item in enumerate(re.finditer(splitter, input)):
            current_item = item.group(1)
            current_item_index = input_index + item.start(1)
            if not (guard and re.match(guard, current_item)):
                all_founds.append((current_item, current_item_index))

        def closest_to_caret(item, caret):
            return min(math.fabs(item[1] - caret), math.fabs(item[1] + len(item[0]) - 1 - caret))

        if all_founds:
            return sorted(all_founds, key=lambda item:closest_to_caret(item, self.region.begin()))[0]
        else:
            return False, False

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

    def get_current_date(self):
        if self.current_value.get('value'):
            return False

        # TODO: make the get_closest_value to return Region
        date, date_index = self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'(\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b)'
            )

        number, number_index = self.get_closest_value(
            date,
            date_index,
            r'(\b\d+\b)'
            )

        if number:
            self.current_value['fullDate'] = date
            if len(number) == 4:
                self.current_value['context'] = 'DateYear'
            elif date_index + 8 - number_index == 0:
                self.current_value['context'] = 'DateDay'
            else:
                self.current_value['context'] = 'DateMonth'

            self.current_value['value'] = number
            self.current_value['region'] = sublime.Region(number_index, number_index + len(number))

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
            r'(((?<![a-zA-Z])-)?[0-9]*((?<![\.])\.)?[0-9]+)'
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

    def rotate_date(self):
        if self.new_value or not self.current_value.get('value') or self.current_value.get('context') != 'Date':
            return False
    def rotate_numeric_value(self):
        if self.new_value or not self.current_value.get('value'):
            return False

        is_Date = self.current_value.get('context') in ['DateYear', 'DateMonth', 'DateDay']

        left_limit = float("-inf")
        right_limit = float("inf")
        if self.current_value.get('prop'):
            if get_key_from_property(self.current_value.get('prop'), 'always_positive'):
                left_limit = float(0)

        if is_Date:
            left_limit = float(1)

        if self.current_value.get('context') == 'DateMonth':
            right_limit = 12

        if self.current_value.get('context') == 'DateDay':
            # Use better algorithm,
            # This somehow dont work at april o_O
            # months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            # right_limit = months[int(re.match(r'^[0-9]+-([0-9]+)', self.current_value.get('fullDate')).group(1)) - 1]
            right_limit = 31
            # When we change the month, we should change the day if it is more than possible

        # Should we allow incrementing month after the day incremented after max? I guess so

        modifier = self.modifier

        if is_Date:
            if modifier > 0:
                modifier = math.ceil(modifier)
            else:
                modifier = math.floor(modifier)

        found_number = re.search(r'^(-?\d*\.?\d+)(.*)$', self.current_value.get('value'))
        if found_number:
            new_value = round(float(found_number.group(1)) + modifier, 13)
            new_value = min(max(left_limit, new_value), right_limit)

            # Check if we need to add mandatory unit
            # replace with postexpand in the future?
            postfix = ''
            prefix = ''
            new_number = ''
            if found_number.group(1) == '0' and found_number.group(2) == '' and self.current_value.get('context') == 'CSS value':
                possible_values = get_key_from_property(self.current_value.get('prop'), 'values')
                if '<dimension>' in possible_values or '<length>' in possible_values:
                    if new_value % 1 == 0:
                        postfix = 'px'
                    else:
                        postfix = 'em'

            new_number = prefix + str(new_value).rstrip('0').rstrip('.') + postfix
            if is_Date:
                new_number = new_number.zfill(len(self.current_value.get('value')))

            self.new_value = new_number + found_number.group(2)
