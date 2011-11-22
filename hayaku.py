# -*- coding: utf-8 -*-
import re
import operator
from functools import partial

import sublime
import sublime_plugin

from probe import extract
from templates import make_template

__all__ = [
    'HayakuCommand',
    'HayakuChangeNumberCommand',
]

# максимальный размер css properties
MAX_SIZE_CSS = len('-webkit-transition-timing-function')

ABBR_REGEX = re.compile(r'[\s|;|{]([:a-z-]+)$', re.IGNORECASE)

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
        # print abbr, 'abbr'
        if ':' in abbr:
            prop_abbr, value_abbr = abbr.split(':')
            prop = extract(prop_abbr)
            prop = extract('{0}{1}'.format(prop, value_abbr))
        else:
            prop = extract(abbr)
            if not prop:
                return

        if ' ' in prop:
            prop, value = prop.split()
            template = make_template(prop, value)
        else:
            template = make_template(prop)

        new_cur_pos = cur_pos-len(abbr)
        assert cur_pos-len(abbr) >= 0
        self.view.erase(edit, sublime.Region(new_cur_pos, cur_pos))
        self.view.run_command("insert_snippet", {"contents": template})

WHITE_SPACE_FINDER = re.compile(r'^(\s*)[-\w].*')
class HayakuAddLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        if len(regions) > 1:
            align_regions = (self.view.line(r) for r in regions)
            strings = (self.view.substr(r) for r in align_regions)
            finders = (WHITE_SPACE_FINDER.search(s) for s in strings)
            min_size = min(len(g.group(1)) for g in finders if g is not None)
            max_pos = max(r.end() for r in regions)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(max_pos, max_pos))
            self.view.run_command('insert', {"characters": "\n"})
            erase_region = self.view.line(self.view.sel()[0])
            reg = sublime.Region(erase_region.a + min_size, erase_region.b)
            self.view.erase(edit, reg)
        else:
            self.view.run_command('insert', {"characters": "\n"})


OPERATION_TABLE = {
    "up": partial(operator.add, 1),
    "down": partial(operator.add, -1),
    "shift_up": partial(operator.add, 10),
    "shift_down": partial(operator.add, -10),
    "alt_up": partial(operator.add, 0.1),
    "alt_down": partial(operator.add, -0.1),
}

# Изменяет число по сочетаниям ctrl/alt/shift + up/down
class HayakuChangeNumberCommand(sublime_plugin.TextCommand):
    def run(self, edit, key):

        # поиск текущей позиции в файле
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

        # Буферы для чисел до и после курсора
        before_buf = []
        after_buf = []

        # считывает линию и текущую позицию в куросора в строке
        line_region = self.view.line(cur_pos)
        line = self.view.substr(line_region)
        row, col = self.view.rowcol(cur_pos)

        for i in range(col-1, 0-1, -1):
            if line[i].isdigit() or line[i] in ('.', '-'):
                before_buf.append(line[i])
            else:
                break
        before_buf = before_buf[::-1]
        for i in range(col, len(line)):
            if line[i].isdigit() or line[i] in ('.', '-'):
                after_buf.append(line[i])
            else:
                break
        
        start_pos_offset = len(before_buf)
        end_pos_offset = len(after_buf)

        # прочитать число
        total_buf = before_buf + after_buf
        buf = u''.join(total_buf)
        value = None
        try:
            value = float(buf)
            value = int(buf)
        except ValueError:
            if value is None:
                return

        # Расчёт нового значения
        operation = OPERATION_TABLE[key]
        new_value = operation(value)

        # Замена региона с числом
        start_pos = cur_pos - start_pos_offset
        end_pos = cur_pos + end_pos_offset
        replace_region = sublime.Region(start_pos, end_pos)
        self.view.replace(edit, replace_region, str(new_value))

        # установить курсор на место
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(cur_pos, cur_pos))


# class DetectHayakuValuesEventListener(sublime_plugin.EventListener):
#     def on_modified(self, view):

#         # поиск текущей позиции в файле
#         regions = view.sel()
#         if len(regions) > 1:
#             # разобраться с многооконными выборками
#             # пока что работаем только с одним регионом
#             for r in regions:
#                 view.insert(edit, r, '\t')
#             return
#         region = regions[0]
#         if not region.empty():
#             # сделать работы с выделенным словом
#             view.insert(edit, region, '\t')
#             return
#         cur_pos = region.begin()

#         st = view.scope_name(cur_pos)
#         if not st.startswith('source.css'):
#             return
    
#         line_num, col_num = view.rowcol(cur_pos)
#         line = view.substr(view.line(cur_pos))

#         # курсор находится в значении css-правила
#         if re.match('.*[:|\s*]$', line[:col_num]) and re.match('^[;|\s*|$].*', line[col_num:]):
#             # Свойство
#             prop = re.match('.*?([A-Za-z-]+):[\s*]?$', line[:col_num])
#             if prop is not None:
#                 import datetime
#                 print prop.group(1), 'prop', datetime.datetime.now()
#                 # from ololo import PROPS
#                 # ch = view.substr(cur_pos)
#                 # values = PROPS[prop]
#                 # if not values:
#                 #     return
                



        
