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
    parse_dict_json = import_dir('css_dict_driver', ('parse_dict_json',)).parse_dict_json
except ImportError:
    from css_dict_driver import parse_dict_json

try:
    get_hayaku_options = import_dir('add_code_block', ('add_code_block',)).get_hayaku_options
except ImportError:
    from add_code_block import get_hayaku_options


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
        template = make_template(args, options)

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
