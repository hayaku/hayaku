# -*- coding: utf-8 -*-
import re
import operator
from functools import partial

import sublime
import sublime_plugin

from core.probe import extract
from core.templates import make_template

__all__ = [
    'HayakuCommand',
]

# максимальный размер css properties
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([\.:%#a-z-,\d]+!?)$', re.IGNORECASE)

GUESS_REGEX = re.compile(r'selector(\s+)?(\{)?(\s+)?property(:)?(\s+)?value(;)?(\s+)?(\})?(\s+)?', re.IGNORECASE)

def get_hayaku_options(self):

    # Autoguessing the options
    settings = self.view.settings()
    options = {}
    match = {}
    if settings.get("hayaku_CSS_syntax_autoguess"):
        autoguess = settings.get("hayaku_CSS_syntax_autoguess")
        offset = len(autoguess[0]) - len(autoguess[0].lstrip())
        autoguess = [ s[offset:].rstrip() for s in autoguess]

        #                            1     2    3            4    5         6    7     8    9
        match = GUESS_REGEX.search('\n'.join(autoguess))

    options["CSS_whitespace_block_start_before"] = settings.get("hayaku_CSS_whitespace_block_start_before", match and match.group(1) or "")
    options["CSS_whitespace_block_start_after"]  = settings.get("hayaku_CSS_whitespace_block_start_after",  match and match.group(3) or "\n\t")
    options["CSS_whitespace_block_end_before"]   = settings.get("hayaku_CSS_whitespace_block_end_before",   match and match.group(7) or "\n\t")
    options["CSS_whitespace_block_end_after"]    = settings.get("hayaku_CSS_whitespace_block_end_after",    match and match.group(9) or "")
    options["CSS_whitespace_after_colon"]        = settings.get("hayaku_CSS_whitespace_after_colon",        match and match.group(5) or "")
    options["CSS_syntax_no_curly_braces"]        = settings.get("hayaku_CSS_syntax_no_curly_braces",        match and not (match.group(2) and match.group(8)) or False)
    options["CSS_syntax_no_colons"]              = settings.get("hayaku_CSS_syntax_no_colons",              match and not match.group(4) or False)
    options["CSS_syntax_no_semicolons"]          = settings.get("hayaku_CSS_syntax_no_semicolons",          match and not match.group(6) or False)
    options["CSS_prefixes_disable"]              = settings.get("hayaku_CSS_prefixes_disable",              False)
    options["CSS_prefixes_align"]                = settings.get("hayaku_CSS_prefixes_align",                True)
    options["CSS_prefixes_only"]                 = settings.get("hayaku_CSS_prefixes_only",                 [])
    options["CSS_prefixes_no_unprefixed"]        = settings.get("hayaku_CSS_prefixes_no_unprefixed",        False)
    options["CSS_disable_postexpand"]            = settings.get("hayaku_CSS_disable_postexpand",            False)

    return options

class HayakuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        if len(regions) > 1:
            # разобраться с многооконными выборками
            # пока что работаем только с одним регионом
            for r in regions:
                self.view.insert(edit, r, '\t')
            return
        region = regions[0]
        if not region.empty():
            # сделать работы с выделенным словом
            self.view.insert(edit, region, '\t')
            return
        cur_pos = region.begin()

        start_pos = cur_pos - MAX_SIZE_CSS
        if start_pos < 0:
            start_pos = 0
        probably_abbr = self.view.substr(sublime.Region(start_pos, cur_pos))
        match = ABBR_REGEX.search(probably_abbr)
        if match is None:
            self.view.insert(edit, cur_pos, '\t')
            return

        abbr = match.group(1)
        args = extract(abbr)
        if not args:
            return

        get_hayaku_options(self)

        options = get_hayaku_options(self)

        template = make_template(args, options)
        if template is None:
            return
        new_cur_pos = cur_pos-len(abbr)
        assert cur_pos-len(abbr) >= 0
        self.view.erase(edit, sublime.Region(new_cur_pos, cur_pos))
        self.view.run_command("insert_snippet", {"contents": template})

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

    if found_indent < first_indent and not is_prefixed_property(view.substr(get_previous_line(view,line_region))) and first_is_ok or is_nested:
        found_indent = found_indent + "    "

    if not found_indent:
        if first_indent:
            found_indent = first_indent
        else:
            found_indent = ""
    return found_indent

class HayakuAddLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        nearest_indent = get_nearest_indent(self.view)
        if len(regions) > 1:
            align_regions = (self.view.line(r) for r in regions)
            strings = (self.view.substr(r) for r in align_regions)
            finders = (WHITE_SPACE_FINDER.search(s) for s in strings)
            min_size = min(len(g.group(1)) for g in finders if g is not None)
            max_pos = max(r.end() for r in regions)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(max_pos, max_pos))
            self.view.run_command('insert', {"characters": "\n"})
            erase_region = self.view.line(self.view.sel()[0])
            reg = sublime.Region(erase_region.a + min_size, erase_region.b)
            self.view.erase(edit, reg)
        else:
            self.view.run_command('insert', {"characters": "\n"})
            self.view.erase(edit, sublime.Region(self.view.line(self.view.sel()[0]).a, self.view.sel()[0].a))
            self.view.run_command('insert', {"characters": nearest_indent})
