#!/usr/bin/python
import re
import sublime
import sublime_plugin

class HayakuStyleContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_css_context":
            return None

        regions = view.sel()
        # We won't do anything for multiple carets for now
        if len(regions) > 1:
            return None

        region = regions[0]

        # We don't do anything for selection for now
        if not region.empty():
            return None

        # Looking for the scope
        # TODO: Make it expandable in HTML's attributes (+ left/right fixes)
        if view.score_selector(region.begin(),'source.css -meta.selector.css, source.stylus, source.sass, source.scss') == 0:
            return None

        # Determining the left and the right parts
        line = view.line(region)
        left_part = view.substr(sublime.Region(line.begin(), region.begin()))
        right_part = view.substr(sublime.Region(region.begin(),line.end()))

        # Simple check if the left part is ok
        # 1. Caret is not straight after semicolon, slash or plus sign
        # 2. We're not at the empty line
        # 3. There were no property/value like entities before caret
        #                  1      2         3
        if re.search('[;\s\/\+]$|^$|[^\s;\{] [^;\{]+$',left_part) is not None:
            return None

        # Simple check if the right part is ok
        # 1. The next symbol after caret is not space or curly brace
        # 2. There could be only full property+value part afterwards
        #                 1           2
        if re.search('^[^\s\}]|^\s[^:\}]+[;\}]',right_part) is not None:
            return None

        return True
