# -*- coding: utf-8 -*-
import os
import re

from itertools import chain, product

import sublime
import sublime_plugin

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)


try:
    extract = import_dir('probe', ('extract',)).extract
except ImportError:
    from probe import extract

try:
    make_template = import_dir('templates', ('make_template',)).make_template
except ImportError:
    from templates import make_template

try:
    get_hayaku_options = import_dir('add_code_block', ('add_code_block',)).get_hayaku_options
except ImportError:
    from add_code_block import get_hayaku_options

try:
    get_values_by_property = import_dir('css_dict_driver', ('get_values_by_property',)).get_values_by_property
except ImportError:
    from css_dict_driver import get_values_by_property

# The maximum size of a single propery to limit the lookbehind
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([\.:%#a-z-,\d]+!?)$', re.IGNORECASE)



class HayakuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        cur_pos = self.view.sel()[0].begin()
        start_pos = cur_pos - MAX_SIZE_CSS
        if start_pos < 0:
            start_pos = 0
        # TODO: Move this to the contexts, it's not needed here
        probably_abbr = self.view.substr(sublime.Region(start_pos, cur_pos))
        match = ABBR_REGEX.search(probably_abbr)
        if match is None:
            self.view.insert(edit, cur_pos, '\t')
            return

        abbr = match.group(1)

        # Extracting the data from the abbr
        args = extract(abbr)

        if not args:
            return

        # Getting the options and making a snippet
        # from the extracted data
        get_hayaku_options(self)
        options = get_hayaku_options(self)
        template = make_template(args, options, sublime.get_clipboard())

        if template is None:
            return

        # Inserting the snippet
        new_cur_pos = cur_pos - len(abbr)
        assert cur_pos - len(abbr) >= 0
        self.view.erase(edit, sublime.Region(new_cur_pos, cur_pos))

        self.view.run_command("insert_snippet", {"contents": template})


# Helpers for getting the right indent for the Add Line Command
WHITE_SPACE_FINDER = re.compile(r'^(\s*)(-)?[\w]*')
def get_line_indent(line):
    return WHITE_SPACE_FINDER.match(line).group(1)

def is_prefixed_property(line):
    return WHITE_SPACE_FINDER.match(line).group(2) is not None

def get_previous_line(view, line_region):
    return view.line(line_region.a - 1)

def get_nearest_indent(view):
    line_region = view.line(view.sel()[0])
    line = view.substr(line_region)
    line_prev_region = get_previous_line(view,line_region)

    found_indent = None
    first_indent = None
    first_is_ok = True
    is_nested = False

    # Can we do smth with all those if-else noodles?
    if not is_prefixed_property(line):
        first_indent = get_line_indent(line)
        if not is_prefixed_property(view.substr(line_prev_region)):
            return first_indent
        if is_prefixed_property(view.substr(line_prev_region)):
            first_is_ok = False
    while not found_indent and line_prev_region != view.line(sublime.Region(0)):
        line_prev = view.substr(line_prev_region)
        if not first_indent:
            if not is_prefixed_property(line_prev):
                first_indent = get_line_indent(line_prev)
                if is_prefixed_property(view.substr(get_previous_line(view,line_prev_region))):
                    first_is_ok = False
        else:
            if not is_prefixed_property(line_prev) and not is_prefixed_property(view.substr(get_previous_line(view,line_prev_region))):
                found_indent = min(first_indent,get_line_indent(line_prev))

        line_prev_region = get_previous_line(view,line_prev_region)
        if line_prev.count("{"):
            is_nested = True

    if found_indent and found_indent < first_indent and not is_prefixed_property(view.substr(get_previous_line(view,line_region))) and first_is_ok or is_nested:
        found_indent = found_indent + "    "

    if not found_indent:
        if first_indent:
            found_indent = first_indent
        else:
            found_indent = ""
    return found_indent

class HayakuAddLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        nearest_indent = get_nearest_indent(self.view)

        # Saving current auto_indent setting
        # This hack fixes ST2's bug with incorrect auto_indent for snippets
        # It seems that with auto indent off it uses right auto_indent there lol.
        current_auto_indent = self.view.settings().get("auto_indent")
        self.view.settings().set("auto_indent",False)

        self.view.run_command('insert', {"characters": "\n"})
        self.view.erase(edit, sublime.Region(self.view.line(self.view.sel()[0]).a, self.view.sel()[0].a))
        self.view.run_command('insert', {"characters": nearest_indent})
        self.view.settings().set("auto_indent",current_auto_indent)


class HayakuCyclingThroughValues(sublime_plugin.TextCommand):
    def run(self, edit, direction, amount = 1):
        # Store the arguments
        self.edit = edit
        self.direction = direction
        self.amount = amount
        self.dirty_regions = []
        regions = enumerate(self.view.sel())

        for index, region in regions:
            self.region = region
            self.region_index = index

            # Check if the current region was in the area where the first one made changes to
            should_proceed = True
            for dirty_region in self.dirty_regions:
                if dirty_region.intersects(region):
                    should_proceed = False

            # Check if the region is multiline
            if self.view.line(self.region) != self.view.line(self.region.begin()):
                should_proceed = False

            if should_proceed:
                self.handle_region()

    def handle_region(self):
        result = self.do_actual_stuff()
        if not result:
            return False

        region, text = result
        self.dirty_regions.append(region)

        # Get the proper offsets according to the rules
        old_position = self.view.sel()[self.region_index]
        offset = len(text) - len(self.view.substr(region))
        offset_start = old_position.begin()
        offset_end = old_position.end()
        region_range = range(region.begin() + 1, region.end())
        if old_position.begin() >= region.end():
            offset_start = offset_start + offset
        elif offset_start in region_range:
            offset_start = offset_start + offset
            if offset_start < region.begin():
                offset_start = region.begin()
        if old_position.end() >= region.end():
            offset_end = offset_end + offset
        elif offset_end in region_range:
            offset_end = offset_end + offset
            if offset_end < region.begin():
                offset_end = region.begin()

        new_position = sublime.Region(offset_start, offset_end)
        position_changed = old_position != new_position
        if position_changed:
            self.view.sel().subtract(old_position)
        self.view.replace(self.edit, region, text)
        if position_changed:
            self.view.sel().add(new_position)

    def do_actual_stuff(self):
        # 0. Getting the context
        region_begin = self.region.begin()
        region_end = self.region.end()

        line_region = self.view.line(self.region)
        line = self.view.substr(line_region)
        line_begin = line_region.begin()
        line_end = line_region.end()

        selection = self.view.substr(self.region)

        # 1. TODO: See if we're at CSS scope and stuff
        # https://github.com/hayaku/hayaku/wiki/Cycling-values
        if True:
            # Getting the proper context out of possible multiple declarations
            # TODO: handle multiline props, when lines ending with `[,\]`, etc?
            # TODO: handle selection somehow
            context_begin = line_begin
            declarations = re.findall(r'([^;]+;?)', line)
            context = None
            for declaration in declarations:
                proper_declaration = not re.match(r'^\s*\/\*|^\W+$', declaration)
                current_declaration = region_begin in range(context_begin, context_begin + len(declaration))

                if proper_declaration:
                    context = declaration

                if current_declaration:
                    if proper_declaration:
                        break
                    else:
                        context_begin = context_begin + len(declaration)

            # Parsed declaration                    prefix        property       delimiter    values
            parsed_declaration = re.search(r'^(\s*)(-[a-zA-Z]+-)?([a-zA-Z0-9-]+)(\s*(?: |\:))((?:(?!\!important).)+)', context)
            context_at_values = region_begin not in range(context_begin, context_begin + parsed_declaration.start(5))
            context_begin = context_begin + parsed_declaration.start(5)

            values = re.finditer(r'([^ ,\(\);]+)', parsed_declaration.group(5))
            prefix = parsed_declaration.group(2)
            prop = parsed_declaration.group(3)
            value = None
            value_context = None
            previous_value = None
            previous_value_begin = None
            previous_value_end = context_begin
            for subvalue in values:
                current_value = subvalue.group(1)
                initial_current_value_begin = context_begin + subvalue.start(1)
                # Adjust begin to the half of the gap with previous item
                current_value_begin = initial_current_value_begin - (initial_current_value_begin - previous_value_end + 1) // 2
                current_value_end = context_begin + subvalue.end(1) + 1

                if not value:
                    value = current_value
                    value_context = initial_current_value_begin
                else:
                    if region_begin in range(previous_value_end, current_value_begin):
                        value = previous_value
                        value_context = previous_value_begin
                        break
                    elif region_begin in range(current_value_begin, current_value_end):
                        value = current_value
                        value_context = initial_current_value_begin
                        break

                previous_value = current_value
                previous_value_end = current_value_end
                previous_value_begin = initial_current_value_begin

        props_values = get_values_by_property(prop)
        index = props_values.index(str(value))
        value_region = sublime.Region(value_context, value_context + len(value))
        assert self.direction in ('up', 'down')
        if self.direction == 'up':
            index += 1
        elif self.direction == 'down':
            index -= 1

        return [value_region, props_values[index % len(props_values)]]
