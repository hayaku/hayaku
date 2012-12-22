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
            initial_offset = regions[0].a - snippet_input.a
            cursor_offset = initial_offset

        snippet_content = self.view.substr(snippet_input)
        snippet_parts = re.split('(\W+)',snippet_content) # the split regex is just a placehoder, would be more complex

        count = 2 # for adding the initial tabstop to mimic the cloning behavior, could be configurable
        count_offset = 0

        for index, part in enumerate(snippet_parts):
            # can this condition be replaced with checking even/oddness?
            if re.match('^\w+$',part):
                snippet_parts[index] = '${' + str(count) + ':' + part + '}'
                count += 1

                if is_single_caret and initial_offset > count_offset:
                    cursor_offset += len(snippet_parts[index]) - len(part)
                    if initial_offset < count_offset + len(part):
                        cursor_offset -= 1

            count_offset += len(part)

        snippet_content = ''.join(snippet_parts)

        # Finding a place where to insert the clone
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
            snippet_result = "${1:" + snippet_content + "}"

        self.view.run_command("insert_snippet", {"contents": snippet_result})

        # Removing an extra newline that were there for indent behavior fixing
        self.view.erase(edit, sublime.Region(target.a + count_offset, target.a + count_offset + 1))

