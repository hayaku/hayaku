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
    get_hayaku_options = import_dir('hayaku_sublime_get_options', ('hayaku_sublime_get_options',)).get_hayaku_options
except ImportError:
    from hayaku_sublime_get_options import get_hayaku_options

class HayakuCyclingThroughValuesCommand(sublime_plugin.TextCommand):
    def run(self, edit, modifier = 1):
        self.edit = edit
        self.options = get_hayaku_options(self)

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
        self.possible_values = []

        # Check if the current region was in the area where the first one made changes to
        should_proceed = not any(dirty_region.intersects(region) for dirty_region in self.dirty_regions)

        if should_proceed:
            self.get_dates()
            self.get_versions()
            self.get_CSS_values()
            self.get_numbers()
            for value in sorted(self.possible_values, key=lambda item:item['proximity']):
                new_value = self.run_all_adjusts(value, [
                    self.adjust_CSS_string,
                    self.adjust_date,
                    self.adjust_version,
                    self.adjust_number
                ])

                if new_value:
                    self.apply_new_value(new_value)
                    break

    def is_multiline(self, region):
        return self.view.line(region) != self.view.line(region.begin())

    def get_new_position(self, cursor_position, value):
        old_region = value.get('old_region')
        new_value = value.get('new_value')
        stay_on_right = not value.get('stay_at_left')
        context_offset = value.get('context_offset')

        def adjust_offset(cursor):
            offset = len(new_value) - len(self.view.substr(old_region))

            if context_offset != None:
                return cursor + context_offset

            if cursor >= old_region.end():
                cursor = cursor + offset
            elif old_region.begin() < cursor <= old_region.end():
                if stay_on_right:
                    cursor = max(cursor + offset, old_region.begin())
                else:
                    cursor = min(cursor, old_region.end() + offset)
            return cursor

        return sublime.Region(
            adjust_offset(cursor_position.begin()),
            adjust_offset(cursor_position.end()))

    def apply_new_value(self, value):
        if not value:
            return
        reselect = self.region_index != None

        if reselect:
            old_position = self.view.sel()[self.region_index]
            new_position = self.get_new_position(old_position, value)

            self.view.sel().subtract(old_position)

        self.view.replace(self.edit, value.get('old_region'), value.get('new_value'))

        if reselect:
            self.dirty_regions.append(value.get('old_region'))

            self.view.sel().add(new_position)

    def get_closest_value(self, input, input_index, splitter, guard=None, extras={}):
        if not input:
            return

        all_founds = []

        for index, item in enumerate(re.finditer(splitter, input)):
            current_item = item.group(1)
            current_item_index = input_index + item.start(1)
            if not (guard and re.match(guard, current_item)):
                cursor_position = self.region.begin()
                proximity = min(
                    math.fabs(current_item_index - cursor_position),
                    math.fabs(current_item_index + len(current_item) - 1 - cursor_position)
                )
                if current_item_index < cursor_position <= current_item_index + len(current_item):
                    proximity = 0

                found_value = {
                    'value': current_item,
                    'index': current_item_index,
                    'proximity': proximity
                }

                for key in extras:
                    found_value[key] = extras[key]

                if found_value.get('region') == True:
                    found_value['region'] = sublime.Region(current_item_index, current_item_index + len(current_item))

                all_founds.append(found_value)

        def closest_to_caret(item, caret):
            return min(math.fabs(item.get('index') - caret), math.fabs(item.get('index') + len(item.get('value')) - 1 - caret))

        return sorted(all_founds, key=lambda item:closest_to_caret(item, self.region.begin()))

    def get_word_likes(self):
        return self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'(\S+)',
            r'(^[^0-9]+$)',
        )

    def get_CSS_declarations(self):
        if not sublime.score_selector(self.view.scope_name(self.region.a), 'source.css, source.less, source.sass, source.scss, source.stylus, source.postcss'):
            return False

        return self.get_closest_value(
            self.view.substr(self.view.line(self.region)),
            self.view.line(self.region).begin(),
            r'([^;]+;?)',
            r'^\s*\/\*|^\W+$'
        )

    def get_CSS_values(self):
        declarations = self.get_CSS_declarations()
        if not declarations:
            return
        for declaration in declarations:
            # Parsed declaration                    prefix        property                         delimiter    values
            parsed_declaration = re.search(r'^(\s*)(-[a-zA-Z]+-)?([a-zA-Z-]*[a-zA-Z][a-zA-Z0-9-]*)(\s*(?: |\:))((?:(?!\!important).)+)', declaration.get('value'))
            if not parsed_declaration:
                continue

            values = self.get_closest_value(
                parsed_declaration.group(5),
                declaration.get('index') + parsed_declaration.start(5),
                r'(#[a-zA-Z0-9]{3,6}|((?<![\w])-)?[0-9]*((?<![\.])\.)?[0-9]+[a-zA-Z%]*|[a-zA-Z\-]+)',
                extras={
                    'region': True,
                    'context': 'CSS value',
                    'prop': parsed_declaration.group(3)
                }
            )
            if values:
                self.possible_values += values

    def get_dates(self):
        word_likes = self.get_word_likes()
        if not word_likes:
            return
        for word_like in word_likes:
            dates = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'(\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b)',
                extras={
                    'region': True,
                    'context': 'Date'
                }
            )
            if dates:
                self.possible_values += dates

    def get_versions(self):
        word_likes = self.get_word_likes()
        if not word_likes:
            return
        for word_like in word_likes:
            versions = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'((([0-9]+|[x*])\.){2,}([0-9]+|[x*])+)',
                extras={
                    'region': True,
                    'context': 'Version'
                }
            )
            if versions:
                self.possible_values += versions

    def get_numbers(self):
        word_likes = self.get_word_likes()
        if not word_likes:
            return
        for word_like in word_likes:
            numbers = self.get_closest_value(
                word_like.get('value'),
                word_like.get('index'),
                r'(((?<![a-zA-Z])-)?[0-9]*((?<![\.])\.)?[0-9]+)',
                extras={
                    'region': True,
                    'context': 'Number'
                }
            )
            if numbers:
                self.possible_values += numbers

    def run_all_adjusts(self, value, adjusts):
        for adjust in adjusts:
            new_value = adjust(value)
            if new_value:
                return new_value

    def adjust_CSS_string(self, value):
        if value.get('context') != 'CSS value':
            return

        props_values = get_values_by_property(value.get('prop'), self.options.get('dict'), include_commented=True)

        # Should we add a setting for allowing toggling from the unknown props?
        if value.get('value') in props_values:
            index = props_values.index(value.get('value'))
            if self.modifier > 0:
                index += 1
            elif self.modifier < 0:
                index -= 1
            found_value = props_values[index % len(props_values)]
            if found_value:
                return {
                    'new_value': found_value,
                    'old_region': value.get('region'),
                    'stay_at_left': True
                }

    def adjust_date(self, value):
        if value.get('context') != 'Date':
            return

        date = value.get('value')
        value_index = value.get('index')
        modifier = self.modifier

        # Detect the context and adjust the modifier
        context = 'Day'
        if self.region.begin() <= value_index + 4:
            context = 'Year'
        elif self.region.begin() <= value_index + 7:
            context = 'Month'

        if context == 'Month':
            if math.fabs(modifier) < 1:
                context = 'Day'
            if math.fabs(modifier) >= 10:
                context = 'Year'
                modifier = int(modifier / math.fabs(modifier))

        elif context == 'Year':
            if math.fabs(modifier) < 1:
                context = 'Month'
                modifier = int(modifier / math.fabs(modifier))

        elif context == 'Day':
            if math.fabs(modifier) >= 10:
                context = 'Month'
                modifier = int(modifier / math.fabs(modifier))

            if modifier > 0:
                modifier = math.ceil(modifier)
            else:
                modifier = math.floor(modifier)

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

        return {
            'new_value': new_date.isoformat(),
            'old_region': value.get('region')
        }

    def adjust_version(self, value):
        if value.get('context') != 'Version':
            return

        modifier = self.modifier

        subversions = self.get_closest_value(
            value.get('value'),
            value.get('index'),
            r'([0-9]+)',
            extras={
                'region': True
            }
        )
        ordered_subversions = sorted(subversions, key=lambda item:item['index'])
        subversion = subversions[0]

        # Select the version based on modifier
        if math.fabs(modifier) < 1:
            subversion = ordered_subversions[max(0, min(len(subversions) - 1, ordered_subversions.index(subversion) + 1))]
        elif math.fabs(modifier) >= 10:
            subversion = ordered_subversions[max(0, min(len(subversions) - 1, ordered_subversions.index(subversion) - 1))]

        if modifier > 0:
            modifier = 1
        else:
            modifier = -1

        return {
            'new_value': str(max(0, int(subversion.get('value')) + modifier)),
            'old_region': subversion.get('region')
        }

    def adjust_number(self, value):
        if not value.get('context') in ['Number', 'CSS value']:
            return

        number = value.get('value')
        context_offset = None
        position_modifier = 1
        found_number = re.search(r'^(-?\d*\.?\d+)(.*)$', number)
        if not found_number:
            return

        old_value = found_number.group(1)
        value_index = value.get('region').a
        initial_context_position = 0

        left_limit = float("-inf")
        right_limit = float("inf")

        is_PositiveProperty = value.get('prop') and get_key_from_property(value.get('prop'), 'always_positive', self.options.get('dict'))
        if is_PositiveProperty:
            left_limit = float(0)

        modifier = self.modifier

        # TODO: Move to a modifier-adjusting function,
        #       so it could be reused in date/version
        # If there is a selection and it contains digit, adjust modifier context
        if not self.multiline and self.region.begin() != self.region.end() and re.match(r'[^0-9]*[0-9]', old_value) and re.match(r'[^0-9]*[0-9]', self.view.substr(self.region)):
            right_bound = max(self.region.begin(), self.region.end())
            if right_bound in range(value_index + 1, value_index + len(old_value) + 1):
                left_part = old_value[:right_bound - value_index]
                right_part = old_value[right_bound - value_index:]
                after_dot = re.match(r'^[^\.]*\.([0-9]+)', left_part)
                before_dot = re.match(r'^([0-9]*)([^0-9]*|[\.\-].*)$', right_part)

                if after_dot:
                    after_dot_length = len(str(after_dot.group(1))) - 1
                    initial_context_position = len(left_part) + after_dot_length
                    position_modifier = float('0.' + '0'*after_dot_length + '1')
                elif before_dot:
                    initial_context_position = len(left_part)
                    position_modifier =  10**len(str(before_dot.group(1)))

                if position_modifier:
                    modifier = modifier * position_modifier

        # TODO: Use another way of handling low values, so no round'd be needed
        new_value = round(float(old_value) + modifier, 11)
        new_value = min(max(left_limit, new_value), right_limit)

        # Check if we need to add mandatory unit
        # replace with postexpand in the future?
        postfix = ''
        if old_value == '0' and found_number.group(2) == '' and value.get('context') == 'CSS value':
            possible_values = get_key_from_property(value.get('prop'), 'values', self.options.get('dict'))
            if '<dimension>' in possible_values or '<length>' in possible_values:
                if new_value % 1 == 0:
                    postfix = 'px'
                else:
                    postfix = 'em'

        new_value = str(new_value).rstrip('0').rstrip('.')
        if initial_context_position:
            extra_symbols = ''

            old_dot_index = None
            if '.' in old_value:
                old_dot_index = old_value.index('.')

            new_dot_index = None
            if '.' in new_value:
                new_dot_index = new_value.index('.')


            if old_dot_index:
                if new_dot_index:
                    context_offset = new_dot_index - old_dot_index
                    extra_symbols = '0' * (len(old_value) - len(new_value) + context_offset)
                elif initial_context_position - old_dot_index > 0:
                    extra_symbols = '.' + '0' * (initial_context_position - old_dot_index - 1)
                    # How to manage this? -0.10 // shift+alt+up == bug
                    # + len(new_value) - old_dot_index

            if not old_dot_index:
                old_dot_index = len(old_value)
            if not new_dot_index:
                new_dot_index = len(new_value)

            context_offset = new_dot_index - old_dot_index

            new_value = new_value + extra_symbols

        new_value = new_value + postfix

        return {
            'new_value': new_value + found_number.group(2),
            'old_region': value.get('region'),
            'context_offset': context_offset
        }
