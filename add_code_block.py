#!/usr/bin/python
import re
import sublime
import sublime_plugin


# __all__ = [
#     'HayakuAddCodeBlockCommand',
#     'HayakuExpandCodeBlockCommand',
# ]

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
    get_setting("CSS_syntax_url_quotes",             (is_stylus or is_sass)     )
    get_setting("CSS_syntax_quote_symbol",           "\""      )  # or "'"
    get_setting("CSS_prefixes_disable",              False     )
    get_setting("CSS_prefixes_align",                not (is_stylus or is_sass) )
    get_setting("CSS_prefixes_only",                 []        )
    get_setting("CSS_prefixes_no_unprefixed",        False     )
    get_setting("CSS_disable_postexpand",            False     )
    get_setting("CSS_units_for_unitless_numbers",    False      )
    get_setting("CSS_colors_case",                   "uppercase" ) # or "lowercase" or "initial"
    get_setting("CSS_colors_length",                 "short"   )   # or "long"      or "initial"
    get_setting("CSS_clipboard_defaults",            ["colors","images"] )

    return options

def hayaku_get_block_snippet(options, inside = False):
    start_before = options["CSS_whitespace_block_start_before"]
    start_after = options["CSS_whitespace_block_start_after"]
    end_before = options["CSS_whitespace_block_end_before"]
    end_after = options["CSS_whitespace_block_end_after"]
    opening_brace = "{"
    closing_brace = "}"

    if options["CSS_syntax_no_curly_braces"]:
        opening_brace = ""
        closing_brace = ""
        start_after = ""
        end_after = ""

    if inside:
        opening_brace = ""
        closing_brace = ""
        start_before = ""
        end_after = ""

    return ''.join([
          start_before
        , opening_brace
        , start_after
        , "$0"
        , end_before
        , closing_brace
        , end_after
    ])

# Command
class HayakuExpandCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # TODO: consume the braces and whitespaces around and inside
        self.view.run_command("insert_snippet", {"contents": hayaku_get_block_snippet(get_hayaku_options(self),True)})

class HayakuAddCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = '/* OVERRIDE ME */'

        # Determine the limits for place searching
        regions = self.view.sel()
        region = regions[0]
        line = self.view.line(region)
        stop_point = self.view.find('[}]\s*',line.begin())
        if stop_point is not None and not (-1, -1):
            end = stop_point.end()
        else:
            end = self.view.find('[^}]*',line.begin()).end()
        where_to_search = self.view.substr(
            sublime.Region(
                line.begin(),
                end
            )
        )

        options = get_hayaku_options(self)

        # Insert a code block if we must
        found_insert_position = re.search('^([^}{]*?[^;,}{\s])\s*(?=\n|$)',where_to_search)
        if found_insert_position is not None:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(len(found_insert_position.group(1)) + line.begin(), len(found_insert_position.group(1)) + line.begin()))

            result = hayaku_get_block_snippet(options)
        else:
            # Place a caret + create a new line otherwise
            # FIXME: the newline is not perfectly inserted. Must rethink it so there wouldn't
            # be replacement of all whitespaces and would be better insertion handling
            found_insert_rule = re.search('^(([^}]*?[^;]?)\s*)(?=\})',where_to_search)
            if found_insert_rule:
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(len(found_insert_rule.group(2)) + line.begin(), len(found_insert_rule.group(1)) + line.begin()))

                result = ''.join([
                      options["CSS_whitespace_block_start_after"]
                    , "$0"
                    , options["CSS_whitespace_block_end_before"]
                ])

        self.view.run_command("insert_snippet", {"contents": result})
