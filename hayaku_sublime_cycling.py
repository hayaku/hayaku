# -*- coding: utf-8 -*-
import os
import re
import math
import datetime
import calendar

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

try:
    get_merged_dict = import_dir('hayaku_sublime_get_merged_dict', ('hayaku_sublime_get_merged_dict',)).get_merged_dict
except ImportError:
    from hayaku_sublime_get_merged_dict import get_merged_dict

class HayakuCyclingThroughValuesCommand(sublime_plugin.TextCommand):
    def run(self, edit, modifier = 1):
        self.edit = edit

        self.dict, self.aliases = get_merged_dict(self.view.settings())

        # Set the modifier from the direction and amount
        self.modifier = modifier

        self.dirty_regions = []
        self.multiline = False
        for index, region in enumerate(self.view.sel()):
            if self.is_multiline(region):
                self.multiline = True
                for line_index in range(0, len(self.view.lines(region))):
                    # Do stuff only if selection on a line contains some non-whitespace chars
                    if len(self.view.substr(self.view.split_by_newlines(self.view.sel()[index])[line_index]).strip()) > 0:
                        # Process the proper line region (after possible previous changes)
                        self.process_region(self.view.lines(self.view.sel()[index])[line_index], None)
                self.multiline = False
            else:
                self.process_region(region, index)

    def process_region(self, region, region_index):
        self.region = region
        self.region_index = region_index
        self.new_value = None
        self.current_value = {}
        self.possible_values = []

        # Check if the current region was in the area where the first one made changes to
        should_proceed = not any(dirty_region.intersects(region) for dirty_region in self.dirty_regions)

        if should_proceed:
            self.get_current_CSS_value()
            self.get_current_numeric_value()

            self.get_dates()
            self.get_versions()

            def closest_to_caret(item):
                return item['proximity']

            all_values = sorted(self.possible_values, key=lambda item:closest_to_caret(item))
            print('')
            print('best_matches:')
            for i in range(0, min(6, len(all_values))):
                print(all_values[i])

            self.rotate_CSS_string()
            self.rotate_numeric_value()
            self.apply_current_value()

    def is_multiline(self, region):
        return self.view.line(region) != self.view.line(region.begin())

    def get_new_position(self, initial_position, detected_region, new_value):
        def adjust_offset(adjusted_offset):
            offset = len(new_value) - len(self.view.substr(detected_region))

            if adjusted_offset >= detected_region.end():
                adjusted_offset = adjusted_offset + offset
            elif detected_region.begin() < adjusted_offset <= detected_region.end():
                if not self.current_value.get('stay_at_left'):
                    adjusted_offset = max(adjusted_offset + offset, detected_region.begin())
            return adjusted_offset

        return sublime.Region(
            adjust_offset(initial_position.begin()),
            adjust_offset(initial_position.end()))

    def apply_current_value(self):
        if not self.new_value:
            return False
        reselect = self.region_index != None

        if reselect:
            old_position = self.view.sel()[self.region_index]
            new_position = self.get_new_position(old_position, self.current_value.get('region'), self.new_value)

            self.view.sel().subtract(old_position)

        self.view.replace(self.edit, self.current_value.get('region'), self.new_value)

        if reselect:
            self.dirty_regions.append(self.current_value.get('region'))

            self.view.sel().add(new_position)

    def get_closest_value(self, input, input_index, splitter, guard=None, extras={}):
        if not input:
            return False, False

        all_founds = []

        for index, item in enumerate(re.finditer(splitter, input)):
            current_item = item.group(1)
            current_item_index = input_index + item.start(1)
            if not (guard and re.match(guard, current_item)):
                cursor_position = self.region.begin()
                found_value = {
                    'value': current_item,
                    'index': current_item_index,
                    'proximity': min(math.fabs(current_item_index - cursor_position), math.fabs(current_item_index + len(current_item) - 1 - cursor_position))
                }

                for key in extras:
                    found_value[key] = extras[key]

                if found_value.get('region') == True:
                    found_value['region'] = sublime.Region(current_item_index, current_item_index + len(current_item))

                all_founds.append(found_value)

        def closest_to_caret(item, caret):
            return min(math.fabs(item.get('index') - caret), math.fabs(item.get('index') + len(item.get('value')) - 1 - caret))

        all_founds = sorted(all_founds, key=lambda item:closest_to_caret(item, self.region.begin()))

        if all_founds:
            return (all_founds[0].get('value'), all_founds[0].get('index'), all_founds)
        else:
            return False, False, None

    def get_current_CSS_value(self):
        if self.current_value.get('value') or not sublime.score_selector(self.view.scope_name(self.region.a), 'source.css, source.less, source.sass, source.scss, source.stylus'):
            return False

        # TODO: think on the get_closest_value to accept Region
        declaration, declaration_index, declarations = self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'([^;]+;?)',
            r'^\s*\/\*|^\W+$'
            )

        if not declaration:
            return False

        # Parsed declaration                    prefix        property                         delimiter    values
        parsed_declaration = re.search(r'^(\s*)(-[a-zA-Z]+-)?([a-zA-Z-]*[a-zA-Z][a-zA-Z0-9-]*)(\s*(?: |\:))((?:(?!\!important).)+)', declaration)
        if not parsed_declaration:
            return False
        declaration_index = declaration_index + parsed_declaration.start(5)

        # TODO: make the get_closest_value to return Region
        value, value_index, values = self.get_closest_value(
            parsed_declaration.group(5),
            declaration_index,
            r'(#[a-zA-Z0-9]{3,6}|((?<![\w])-)?[0-9]*((?<![\.])\.)?[0-9]+[a-zA-Z%]*|[a-zA-Z\-]+)',
            extras={
                'region': True,
                'context': 'CSS value',
                'prop': parsed_declaration.group(3)
            }
        )
        self.possible_values += values
        if value:
            self.current_value['context'] = 'CSS value'
            self.current_value['value'] = value
            self.current_value['region'] = sublime.Region(value_index, value_index + len(value))
            self.current_value['prop'] = parsed_declaration.group(3)

    def get_word_likes(self):
        return self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'(\S+)',
            r'(^[^0-9]+$)',
        )[2]

    def get_dates(self):
        for word_like in self.get_word_likes():
            dates = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'(\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b)',
                extras={
                    'region': True,
                    'context': 'Date'
                }
            )
            if dates[2]:
                self.possible_values += dates[2]

    def get_versions(self):
        for word_like in self.get_word_likes():
            versions = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'((([0-9]+|[x*])\.){2,}([0-9]+|[x*])+)',
                extras={
                    'region': True,
                    'context': 'Version'
                }
            )
            if versions[2]:
                self.possible_values += versions[2]

    def get_numbers(self):
        for word_like in self.get_word_likes():
            numbers = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'(((?<![a-zA-Z])-)?[0-9]*((?<![\.])\.)?[0-9]+)',
                extras={
                    'region': True,
                    'context': 'Number'
                }
            )
            if numbers[2]:
                self.possible_values += numbers[2]

    def get_current_numeric_value(self):
        if self.current_value.get('value'):
            return False

        input_string = self.view.substr(self.view.line(self.region))
        input_index = self.view.line(self.region).begin()
        # TODO: make the get_closest_value to return Region
        word_like, word_like_index, word_likes = self.get_closest_value(
            input_string,
            input_index,
            r'(\S+)',
            r'(^[^0-9]+$)',
            )

        # TODO: make the get_closest_value to return Region
        date, date_index, dates = self.get_closest_value(
            word_like,
            word_like_index,
            r'(\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b)'
            )

        # TODO: make the get_closest_value to return Region
        # Add proper versions regexp, as there could be many different variants
        version, version_index, versions = self.get_closest_value(
            word_like,
            word_like_index,
            r'((([0-9]+|[x*])\.){2,}([0-9]+|[x*])+)'
            )

        if version:
            number, number_index, numbers = self.get_closest_value(
                version,
                version_index,
                r'(\b\d+\b)',
                extras={
                    'region': True,
                    'context': 'Version'
                }
            )
            if number:
                self.current_value['context'] = 'Version'
        elif date:
            number, number_index, numbers = self.get_closest_value(
                date,
                date_index,
                r'(\b\d+\b)'
                )
            if number:
                self.current_value['context'] = 'Date'
                if len(number) == 4:
                    self.current_value['subContext'] = 'Year'
                elif date_index + 8 - number_index == 0:
                    self.current_value['subContext'] = 'Day'
                else:
                    self.current_value['subContext'] = 'Month'
            number = date
            number_index = date_index
        else:
            # TODO: make the get_closest_value to return Region
            number, number_index, numbers = self.get_closest_value(
                word_like,
                word_like_index,
                r'(((?<![a-zA-Z])-)?[0-9]*((?<![\.])\.)?[0-9]+)'
                )
            if number:
                self.current_value['context'] = 'Number'

        if number:
            self.current_value['value'] = number
            self.current_value['region'] = sublime.Region(number_index, number_index + len(number))


    def rotate_CSS_string(self):
        if self.new_value or not (self.current_value.get('value') and self.current_value.get('prop')):
            return False

        props_values = get_values_by_property(self.current_value.get('prop'), self.dict, include_commented=True)
        if self.current_value.get('value') in props_values:
            index = props_values.index(self.current_value.get('value'))
            if self.modifier > 0:
                index += 1
            elif self.modifier < 0:
                index -= 1
            # else we should edit it
            self.new_value = props_values[index % len(props_values)]
            self.current_value['stay_at_left'] = True

    def rotate_numeric_value(self):
        value = self.current_value.get('value')
        if self.new_value or not value:
            return False

        value_index = self.current_value.get('region').a
        is_Date = self.current_value.get('context') == 'Date'
        is_Version = self.current_value.get('context') == 'Version'
        is_PositiveProperty = self.current_value.get('prop') and get_key_from_property(self.current_value.get('prop'), 'always_positive', self.dict)

        left_limit = float("-inf")
        right_limit = float("inf")
        if is_Version or is_PositiveProperty:
            left_limit = float(0)

        modifier = self.modifier
        ensure_width = 0

        # If there is a selection and it contains digit, adjust modifier context
        if not self.multiline and self.region.begin() != self.region.end() and re.match(r'[^0-9]*[0-9]', value) and re.match(r'[^0-9]*[0-9]', self.view.substr(self.region)):
            right_bound = max(self.region.begin(), self.region.end())
            if right_bound in range(value_index + 1, value_index + len(value) + 1):
                sign = int(modifier / math.fabs(modifier))
                if value[0] == '-' and not '-' in self.view.substr(self.region):
                    sign = -1 * sign

                left_part = value[:right_bound - value_index]
                right_part = value[right_bound - value_index:]
                after_dot = re.match(r'^[^\.]*\.([0-9]+)', left_part)
                before_dot = re.match(r'^([0-9]+)([^0-9]*|[\.\-].*)$', right_part)
                if after_dot:
                    modifier = sign * math.fabs(modifier * 0.1**len(str(after_dot.group(1))))
                elif before_dot:
                    modifier = sign * math.fabs(modifier * 10**len(str(before_dot.group(1))))
        context = self.current_value.get('subContext')

        if context == 'Month':
            if math.fabs(modifier) < 1:
                context = 'Day'
            if math.fabs(modifier) >= 10:
                context = 'Year'
                modifier = int(modifier / math.fabs(modifier))

        if context == 'Year':
            if math.fabs(modifier) < 1:
                context = 'Month'
                modifier = int(modifier / math.fabs(modifier))

        if context == 'Day':
            if math.fabs(modifier) >= 10:
                context = 'Month'
                modifier = int(modifier / math.fabs(modifier))

        if is_Version or (is_Date and context == 'Day'):
            if modifier > 0:
                modifier = math.ceil(modifier)
            else:
                modifier = math.floor(modifier)

        if is_Date:
            date = value
            # TODO: parse different kinds of dates there (now only iso is supported)
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:10])
            new_date = datetime.date(year, min(month, 12), min(day, calendar.monthrange(year, min(month, 12))[1]))

            if context == 'Day':
                new_date += datetime.timedelta(days=modifier)
            elif context == 'Month':
                month = month - 1 + int(modifier)
                year = year + math.floor(month / 12)
                month = month % 12 + 1
                day = min(day, calendar.monthrange(year, month)[1])
                new_date = datetime.date(year, month, day)
            elif context == 'Year':
                year = year + int(modifier)
                day = min(day, calendar.monthrange(year, month)[1])
                new_date = datetime.date(year, month, day)

            self.new_value = new_date.isoformat()
            return

        found_number = re.search(r'^(-?\d*\.?\d+)(.*)$', value)
        if found_number:
            # TODO: Use another way of handling low values, so no round'd be needed
            new_value = round(float(found_number.group(1)) + modifier, 11)
            new_value = min(max(left_limit, new_value), right_limit)

            # Check if we need to add mandatory unit
            # replace with postexpand in the future?
            postfix = ''
            prefix = ''
            new_number = ''
            if found_number.group(1) == '0' and found_number.group(2) == '' and self.current_value.get('context') == 'CSS value':
                possible_values = get_key_from_property(self.current_value.get('prop'), 'values', self.dict)
                if '<dimension>' in possible_values or '<length>' in possible_values:
                    if new_value % 1 == 0:
                        postfix = 'px'
                    else:
                        postfix = 'em'

            new_number = prefix + str(new_value).rstrip('0').rstrip('.') + postfix

            self.new_value = new_number + found_number.group(2)
