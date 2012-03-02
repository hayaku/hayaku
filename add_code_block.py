#!/usr/bin/python
import re
import sublime
import sublime_plugin

__all__ = [
    'HayakuAddCodeBlockCommand',
]

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
        if view.score_selector(region.begin(),'source.css -meta.property-list.css') == 0:
            return None

        # TODO: add some semantic parsing to understand where we must expand it

        return True

# Command
class HayakuAddCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):

    	snippet = ''.join([
              self.view.settings().get("hayaku_CSS_whitespace_block_start_before")
            , "{"
            , self.view.settings().get("hayaku_CSS_whitespace_block_start_after")
            , "$0"
            , self.view.settings().get("hayaku_CSS_whitespace_block_end_before")
            , "}"
            , self.view.settings().get("hayaku_CSS_whitespace_block_end_after")
        ])

        self.view.run_command("insert_snippet", {"contents": snippet})



