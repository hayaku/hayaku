# -*- coding: utf-8 -*-
import os
import functools
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
    make_template = import_dir('hayaku_templates', ('make_template',)).make_template
except ImportError:
    from hayaku_templates import make_template

try:
    get_css_dict = import_dir('hayaku_dict_driver', ('parse_dict_json',)).get_css_dict
except ImportError:
    from hayaku_dict_driver import get_css_dict

try:
    get_hayaku_options = import_dir('hayaku_sublime_get_options', ('hayaku_sublime_get_options',)).get_hayaku_options
except ImportError:
    from hayaku_sublime_get_options import get_hayaku_options

# The maximum size of a single propery to limit the lookbehind
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([\.:%#a-z-,\d]+!?)$', re.IGNORECASE)

extend_dict_settings = None


class HayakuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit

        self.hayaku = {}
        self.hayaku['options'] = get_hayaku_options(self)
        self.hayaku['abbr'] = self.retrieve_abbr()
        self.hayaku['clipboard'] = sublime.get_clipboard()

        # Extracting the data from the abbr
        self.snippet = make_template(self.hayaku)

        if self.snippet is None:
            return

        self.insert_snippet()

    def retrieve_abbr(self):
        cur_pos = self.view.sel()[0].begin()
        start_pos = cur_pos - MAX_SIZE_CSS
        if start_pos < 0:
            start_pos = 0
        # TODO: Move this to the contexts, it's not needed here
        probably_abbr = self.view.substr(sublime.Region(start_pos, cur_pos))
        match = ABBR_REGEX.search(probably_abbr)
        if match is None:
            self.view.insert(self.edit, cur_pos, '\t')
            return None

        return match.group(1)

    def insert_snippet(self):
        # Inserting the snippet
        cur_pos = self.view.sel()[0].begin()
        new_cur_pos = cur_pos - len(self.hayaku.get('abbr'))
        assert cur_pos - len(self.hayaku.get('abbr')) >= 0
        self.view.erase(self.edit, sublime.Region(new_cur_pos, cur_pos))
        self.view.run_command("insert_snippet", {"contents": self.snippet})

def plugin_loaded():
    global extend_dict_settings
    extend_dict_settings = sublime.load_settings('ExtendDict.sublime-settings')
    extend_dict = extend_dict_settings.get('hayaku_extend_dict')
    if extend_dict is None:
        raise RuntimeError('API is not ready to use')
    func = functools.partial(get_css_dict, True, extend_dict['css'])
    extend_dict_settings.add_on_change('hayaku_extend_dict', func)

try:
    plugin_loaded()
except RuntimeError:
    pass
