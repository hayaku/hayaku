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
        if re.search('[;\s\/\+]$|^$',left_part) is not None:
            return None
        # Simple check if the right part is ok
        # Need to be enhanced to allow one-line coding and comments
        if re.search('^[^\s\}]',right_part) is not None:
            return None

        return True
