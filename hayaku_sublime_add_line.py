# -*- coding: utf-8 -*-
import re
import sublime
import sublime_plugin

# Helpers for getting the right indent for the Add Line Command
WHITE_SPACE_FINDER = re.compile(r'^(\s*)(-)?[\w]*')
class HayakuAddLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        nearest_indent = self.get_nearest_indent()

        # Saving current auto_indent setting
        # This hack fixes ST2's bug with incorrect auto_indent for snippets
        # It seems that with auto indent off it uses right auto_indent there lol.
        current_auto_indent = self.view.settings().get("auto_indent")
        self.view.settings().set("auto_indent",False)

        self.view.run_command('insert', {"characters": "\n"})
        self.view.erase(edit, sublime.Region(self.view.line(self.view.sel()[0]).a, self.view.sel()[0].a))
        self.view.run_command('insert', {"characters": nearest_indent})
        self.view.settings().set("auto_indent",current_auto_indent)

    def get_line_indent(self, line):
        return WHITE_SPACE_FINDER.match(self.view.substr(line)).group(1)

    def is_prefixed_property(self, line):
        return WHITE_SPACE_FINDER.match(self.view.substr(line)).group(2) is not None

    def get_previous_line(self, line_region):
        return self.view.line(line_region.a - 1)

    def get_nearest_indent(self):
        view = self.view
        line_region = view.line(view.sel()[0])
        line_prev_region = self.get_previous_line(line_region)

        found_indent = None
        first_indent = None
        first_is_ok = True
        is_nested = False

        # Can we do smth with all those if-else noodles?
        if not self.is_prefixed_property(line_region):
            first_indent = self.get_line_indent(line_region)
            if not self.is_prefixed_property(line_prev_region):
                return first_indent
            if self.is_prefixed_property(line_prev_region):
                first_is_ok = False
        while not found_indent and line_prev_region != view.line(sublime.Region(0)):
            if not first_indent:
                if not self.is_prefixed_property(line_prev_region):
                    first_indent = self.get_line_indent(line_prev_region)
                    if self.is_prefixed_property(self.get_previous_line(line_prev_region)):
                        first_is_ok = False
            else:
                if not self.is_prefixed_property(line_prev_region) and not self.is_prefixed_property(self.get_previous_line(line_prev_region)):
                    found_indent = min(first_indent, self.get_line_indent(line_prev_region))

            line_prev_region = self.get_previous_line(line_prev_region)
            if view.substr(line_prev_region).count("{"):
                is_nested = True

        if found_indent and found_indent < first_indent and not self.is_prefixed_property(self.get_previous_line(line_region)) and first_is_ok or is_nested:
            found_indent = found_indent + "    "

        if not found_indent:
            if first_indent:
                found_indent = first_indent
            else:
                found_indent = ""
        return found_indent
