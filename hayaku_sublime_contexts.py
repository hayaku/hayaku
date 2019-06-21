#!/usr/bin/python
import re
import sublime
import sublime_plugin

REGEX_WHITESPACES = re.compile(r'^\s*$')

class HayakuSingleCaretContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_single_caret":
            return None

        # Multiple blocks inserting doesn't make sense
        if len(view.sel()) > 1:
            return None

        # TODO: understand selection, but don't replace it on code block inserting
        if not view.sel()[0].empty():
            return None

        return True

class HayakuAtCssContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_at_css":
            return None

        # Looking for the scope
        if not view.score_selector(view.sel()[0].begin(),'source.css, source.stylus, source.sass, source.scss, source.less, source.postcss, source.css.embedded.js'):
            return None

        return True

class HayakuAddCodeBlockContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_add_code_block":
            return None

        # Determining the left and the right parts
        region = view.sel()[0]
        line = view.line(region)
        left_part = view.substr(sublime.Region(line.begin(), region.begin()))
        right_part = view.substr(sublime.Region(region.begin(), line.end()))

        # Check if the line isn't just a line of whitespace
        if REGEX_WHITESPACES.search(left_part + right_part) is not None:
            return None
        # Simple check if the left part is ok
        if left_part.find(';') != -1:
            return None
        # Simple check if the right part is ok
        if right_part.find(';') != -1:
            return None

        return True

class HayakuAddLineContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_add_line":
            return None

        # Determining the left and the right parts
        region = view.sel()[0]
        line = view.line(region)
        left_part = view.substr(sublime.Region(line.begin(), region.begin()))
        right_part = view.substr(sublime.Region(region.begin(), line.end()))

        # Simple check if the left part is ok
        if re.search(';\s*$|[^\s;\{] [^;\{]+$',left_part) is None:
            return None

        # Simple check if the right part is ok
        if re.search('^\s*\}?$',right_part) is None:
            return None

        return True


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
        if view.score_selector(region.begin(),'source.css -meta.selector.css, source.stylus, source.sass, source.scss, source.less, source.postcss, source.css.embedded.js') == 0:
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

# Context-commands to jump out of multiple selections in snippets
class HayakuGoingUpContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_going_up":
            return None
        if len(view.sel()) > 1:
            region = view.sel()[0]
            view.sel().clear()
            view.sel().add(region)
        return None

class HayakuGoingDownContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_going_down":
            return None
        if len(view.sel()) > 1:
            region = view.sel()[1]
            view.sel().clear()
            view.sel().add(region)
        return None
