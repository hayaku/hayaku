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
    get_merged_dict = import_dir('hayaku_get_merged_dict', ('hayaku_get_merged_dict',)).get_merged_dict
except ImportError:
    from hayaku_get_merged_dict import get_merged_dict

# Guessing the codestyle             1     2    3            4    5         6    7     8    9
GUESS_REGEX = re.compile(r'selector(\s*)(\{)?(\s*)property(:)?(\s*)value(;)?(\s*)(\})?(\s*)', re.IGNORECASE)

def get_hayaku_options(self):
    options = {}
    match = {}
    options['settings'] = settings = self.view.settings()

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
        single_setting = None
        if settings.has("hayaku_" + setting):
            single_setting = settings.get("hayaku_" + setting)
        if single_setting is None:
            single_setting = fallback
        options[setting] = single_setting

    # Some hardcode for different scopes
    # (could this be defined better?)
    scope_name = self.view.scope_name(self.view.sel()[0].a)
    scopes = {
        'source.sass': 'Sass',
        'source.stylus': 'Stylus',
        'source.scss': 'SCSS',
        'source.less': 'Less',
        'source.postcss': 'PostCSS'
    }
    for name in scopes:
         if sublime.score_selector(scope_name, name) > 0:
            options['CSS_preprocessor'] = scopes[name]
            break

    syntax_on_indents = options.get('CSS_preprocessor') in ('Stylus', 'Sass')

    disable_braces = syntax_on_indents
    if options.get('CSS_preprocessor') == 'Stylus' and match and match.group(2) and match.group(8):
        disable_braces = False

    disable_colons = options.get('CSS_preprocessor') == 'Stylus'
    if match and match.group(4):
        disable_colons = False

    disable_semicolons = syntax_on_indents
    if options.get('CSS_preprocessor') == 'Stylus' and match and match.group(6):
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
    get_setting("CSS_syntax_url_quotes",             syntax_on_indents     )
    get_setting("CSS_syntax_quote_symbol",           "\""      )  # or "'"
    get_setting("CSS_prefixes_disable",              False     )
    get_setting("CSS_prefixes_align",                not syntax_on_indents )
    get_setting("CSS_prefixes_only",                 []        )
    get_setting("CSS_prefixes_no_unprefixed",        False     )
    get_setting("CSS_disable_postexpand",            False     )
    get_setting("CSS_units_for_unitless_numbers",    False      )
    get_setting("CSS_colors_case",                   "uppercase" ) # or "lowercase" or "initial"
    get_setting("CSS_colors_length",                 "short"   )   # or "long"      or "initial"
    get_setting("CSS_clipboard_defaults",            ["colors","images"] )

    # Retrieving dict and aliases
    options['dict'], options['aliases'] = get_merged_dict(options)

    return options
