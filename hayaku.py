# -*- coding: utf-8 -*-
import re
import sublime
import sublime_plugin

from probe import extract
from templates import make_template

__all__ = [
    'HayakuCommand',
]

# The maximum size of a single propery to limit the lookbehind
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([\.:%#a-z-,\d]+!?)$', re.IGNORECASE)

# Guessing the codestyle             1     2    3            4    5         6    7     8    9
GUESS_REGEX = re.compile(r'selector(\s*)(\{)?(\s*)property(:)?(\s*)value(;)?(\s*)(\})?(\s*)', re.IGNORECASE)


def get_hayaku_options(self):
    settings = self.view.settings()
    options = {}
    match = {}
    # Autoguessing the options
    if settings.get("hayaku_CSS_syntax_autoguess"):
        autoguess = settings.get("hayaku_CSS_syntax_autoguess")
        offset = len(autoguess[0]) - len(autoguess[0].lstrip())
        autoguess = [ s[offset:].rstrip() for s in autoguess]

        match = GUESS_REGEX.search('\n'.join(autoguess))

    # Helper to set an option got from multiple sources
    def get_setting(setting, fallback, match_group = False):
        if match_group and match:
            fallback = match.group(match_group)
        single_setting = False
        if settings.has("hayaku_" + setting):
            single_setting = settings.get("hayaku_" + setting, fallback)
        options[setting] = single_setting or fallback

    # Some hardcode for different scopes
    # (could this be defined better?)
    scope_name = self.view.scope_name(self.view.sel()[0].a)
    is_sass = sublime.score_selector(scope_name, 'source.sass') > 0
    is_stylus = sublime.score_selector(scope_name, 'source.stylus') > 0

    disable_braces = is_stylus or is_sass
    if is_stylus and match and match.group(2) and match.group(8):
        disable_braces = False

    disable_colons = is_stylus
    if match and match.group(4):
        disable_colons = False

    disable_semicolons = is_stylus or is_sass
    if is_stylus and match and match.group(6):
        disable_semicolons = False

    # Calling helper, getting all the needed options
    get_setting("CSS_whitespace_block_start_before", " ",    1 )
    get_setting("CSS_whitespace_block_start_after",  "\n\t", 3 )
    get_setting("CSS_whitespace_block_end_before",   "\n",   7 )
    get_setting("CSS_whitespace_block_end_after",    "",     9 )
    get_setting("CSS_whitespace_after_colon",        " ",    5 )
    get_setting("CSS_newline_after_expand",          False)
    get_setting("CSS_syntax_no_curly_braces",        disable_braces )
    get_setting("CSS_syntax_no_colons",              disable_colons )
    get_setting("CSS_syntax_no_semicolons",          disable_semicolons )
    get_setting("CSS_prefixes_disable",              False     )
    get_setting("CSS_prefixes_align",                not (is_stylus or is_sass) )
    get_setting("CSS_prefixes_only",                 []        )
    get_setting("CSS_prefixes_no_unprefixed",        False     )
    get_setting("CSS_disable_postexpand",            False     )
    get_setting("CSS_colors_case",                   "uppercase" ) # or "lowercase" or "initial"
    get_setting("CSS_colors_length",                 "short"   )   # or "long"      or "initial"
    get_setting("CSS_clipboard_defaults",            ["colors","images"] )

    return options


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
