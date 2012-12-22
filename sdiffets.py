# -*- coding: utf-8 -*-
import re
import sublime
import sublime_plugin

__all__ = [
    'HayakuSdiffetsCommand',
]


class HayakuSdiffetsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        snippet_input = regions[0]

        is_single_caret = snippet_input.a == snippet_input.b
        if is_single_caret:
            snippet_input = self.view.full_line(regions[0])
            cursor_offset = regions[0].a - snippet_input.a

        snippet_content = self.view.substr(snippet_input)

        target = sublime.Region(max(snippet_input.a,snippet_input.b))

        # Creating a new line — without it there are strange things happening with the indents
        self.view.insert(edit, target.a, '\n')

        # Placing cursor where we would insert the snippet
        regions.clear()
        regions.add(target)

        if is_single_caret:
            # the offset would be changed according to the added snippets
            snippet_result = snippet_content[:cursor_offset] + '$1' + snippet_content[cursor_offset:]
        else:
            snippet_result = "${1:" + re.sub('\$','\$',re.sub('}','\}',snippet_content)) + "}"

        self.view.run_command("insert_snippet", {"contents": snippet_result})

        # Removing an extra newline that were there for indent behavior fixing
        self.view.erase(edit, sublime.Region(target.a + len(snippet_content),target.a + len(snippet_content) + 1))

