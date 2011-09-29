# -*- coding: utf-8 -*-
import re

import sublime
import sublime_plugin

__all__ = [
    'HayakuCommand',
]

STATIC_ABBR_DICT = [
    ('z', 'z-index'),
    ('w', 'width'),
    ('t', 'top'),
    ('r', 'right'),
    ('l', 'left'),
    ('b', 'bottom'),
    ('m', 'margin'),
    ('p', 'padding'),
    ('h', 'height'),
    ('q', 'quotes'),
    ('f', 'font')
]

STATIC_ABBR = dict(STATIC_ABBR_DICT)

# максимальный размер css properties
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([a-z-]+)$', re.IGNORECASE)

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
        if abbr in STATIC_ABBR:
            new_cur_pos = cur_pos-len(abbr)
            assert cur_pos-len(abbr) >= 0
            self.view.erase(edit, sublime.Region(new_cur_pos, cur_pos))
            self.view.insert(edit, new_cur_pos, STATIC_ABBR[abbr])
