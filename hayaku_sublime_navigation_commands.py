#!/usr/bin/python
import os
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
    get_hayaku_options = import_dir('hayaku_sublime_get_options', ('hayaku_sublime_get_options',)).get_hayaku_options
except ImportError:
    from hayaku_sublime_get_options import get_hayaku_options

def hayaku_get_block_snippet(options, inside=False):
    start_before = options["CSS_whitespace_block_start_before"]
    start_after = options["CSS_whitespace_block_start_after"]
    end_before = options["CSS_whitespace_block_end_before"]
    end_after = options["CSS_whitespace_block_end_after"]
    opening_brace = "{"
    closing_brace = "}"

    if options["CSS_syntax_no_curly_braces"]:
        opening_brace = ""
        closing_brace = ""
        if '\n' in start_before:
            start_after = ""
        end_after = ""

    if inside:
        opening_brace = ""
        closing_brace = ""
        start_before = ""
        end_after = ""

    return ''.join([
        start_before,
        opening_brace,
        start_after,
        "$0",
        end_before,
        closing_brace,
        end_after
    ])

# Command
class HayakuExpandCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # TODO: consume the braces and whitespaces around and inside
        self.view.run_command("insert_snippet", {"contents": hayaku_get_block_snippet(get_hayaku_options(self),True)})

class HayakuAddCodeBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        result = None

        # Determine the limits for place searching
        regions = self.view.sel()
        region = regions[0]
        line = self.view.line(region)
        stop_point = self.view.find('[}]\s*',line.begin())
        if stop_point is not None and not (-1, -1):
            end = stop_point.end()
        else:
            end = self.view.find('[^}]*',line.begin()).end()
        where_to_search = self.view.substr(
            sublime.Region(
                line.begin(),
                end
            )
        )

        options = get_hayaku_options(self)

        # Insert a code block if we must
        found_insert_position = re.search('^([^}{]*?[^;,}{\s])\s*(?=\n|$)', where_to_search)
        if found_insert_position is not None:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(len(found_insert_position.group(1)) + line.begin(), len(found_insert_position.group(1)) + line.begin()))

            result = hayaku_get_block_snippet(options)
        else:
            # Place a caret + create a new line otherwise
            # FIXME: the newline is not perfectly inserted. Must rethink it so there wouldn't
            # be replacement of all whitespaces and would be better insertion handling
            found_insert_rule = re.search('^(([^}]*?[^;]?)\s*)(?=\})', where_to_search)
            if found_insert_rule is not None:
                self.view.sel().clear()
                self.view.sel().add(sublime.Region(len(found_insert_rule.group(2)) + line.begin(), len(found_insert_rule.group(1)) + line.begin()))

                result = ''.join([
                      options["CSS_whitespace_block_start_after"]
                    , "$0"
                    , options["CSS_whitespace_block_end_before"]
                ])
        assert result is not None
        self.view.run_command("insert_snippet", {"contents": result})

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
