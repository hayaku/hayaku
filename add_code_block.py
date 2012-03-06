#!/usr/bin/python
import re
import sublime
import sublime_plugin

__all__ = [
    'HayakuAddCodeBlockContext',
    'HayakuAddCodeBlockCommand',
]

REGEX_WHITESPACES = re.compile(r'^\s*$')

# Context
class HayakuAddCodeBlockContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
        if key != "hayaku_add_code_block":
            return None

        regions = view.sel()
        # Multiple blocks inserting doesn't make sense
        if len(regions) > 1:
            return None

        region = regions[0]

        # TODO: understand selection, but don't replace it on code block inserting
        if not region.empty():
            return None

        # Looking for the scope
        # TODO: Ensure it would be nice in preprocessors etc.
        if not view.score_selector(region.begin(),'source.css'):
            return None

        # Determining the left and the right parts
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

# Command
class HayakuAddCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = '/* OVERRIDE ME */'

        # Determine the limits for place searching
        regions = self.view.sel()
        region = regions[0]
        line = self.view.line(region)
        stop_point = self.view.find('[}]\s*',line.begin())
        if stop_point is not None:
            end = stop_point.end()
        else:
            end = self.view.find('[^}]*',line.begin()).end()
        where_to_search = self.view.substr(
            sublime.Region(
                line.begin(),
                end
            )
        )

        # Insert a code block if we must
        found_insert_position = re.search('^([^}{]*?[^;,}{\s])\s*(?=\n|$)',where_to_search)
        if found_insert_position is not None:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(len(found_insert_position.group(1)) + line.begin(), len(found_insert_position.group(1)) + line.begin()))

            result = ''.join([
                  self.view.settings().get("hayaku_CSS_whitespace_block_start_before")
                , "{"
                , self.view.settings().get("hayaku_CSS_whitespace_block_start_after")
                , "$0"
                , self.view.settings().get("hayaku_CSS_whitespace_block_end_before")
                , "}"
                , self.view.settings().get("hayaku_CSS_whitespace_block_end_after")
            ])
        else:
            # Place a caret + create a new line otherwise
            # FIXME: the newline is not perfectly inserted. Must rethink it so there wouldn't
            # be replacement of all whitespaces and would be better insertion handling
            found_insert_rule = re.search('^(([^}]*?[^;]?)\s*)(?=\})',where_to_search)
            if found_insert_rule:
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(len(found_insert_rule.group(2)) + line.begin(), len(found_insert_rule.group(1)) + line.begin()))

                result = ''.join([
                      self.view.settings().get("hayaku_CSS_whitespace_block_start_after")
                    , "$0"
                    , self.view.settings().get("hayaku_CSS_whitespace_block_end_before")
                ])

        self.view.run_command("insert_snippet", {"contents": result})
