# -*- coding: utf-8 -*-
# (c) 2012 Sergey Mezentsev
import os
import re
from itertools import product, chain

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)


try:
    imp = import_dir('css_dict_driver', ('css_defaults', 'get_css_dict', 'get_flat_css', 'css_flat_list'))
    css_defaults = imp.css_defaults
    get_css_dict = imp.get_css_dict
    get_flat_css = imp.get_flat_css
    css_flat_list = imp.css_flat_list
except ImportError:
    from css_dict_driver import css_defaults, get_css_dict, get_flat_css, css_flat_list

# TODO: Move this to dicts etc.
PRIORITY_PROPERTIES = [ 'display', 'color', 'margin', 'position', 'padding', 'width', 'background', 'zoom', 'height', 'top', 'vertical-align', 'overflow', 'left', 'margin-right', 'float', 'margin-left', 'cursor', 'text-decoration', 'font-size', 'margin-top', 'border', 'background-position', 'font', 'margin-bottom', 'padding-left', 'right', 'padding-right', 'line-height', 'white-space', 'text-align', 'border-color', 'padding-top', 'z-index', 'border-bottom', 'visibility', 'border-radius', 'padding-bottom', 'font-weight', 'clear', 'max-width', 'border-top', 'border-width', 'content', 'bottom', 'background-color', 'opacity', 'background-image', 'box-shadow', 'border-collapse', 'text-overflow', 'filter', 'border-right', 'text-indent', 'clip', 'min-width', 'min-height', 'border-left', 'max-height', 'border-right-color', 'border-top-color', 'transition', 'resize', 'overflow-x', 'list-style', 'word-wrap', 'border-left-color', 'word-spacing', 'background-repeat', 'user-select', 'border-bottom-color', 'box-sizing', 'border-top-left-radius', 'font-family', 'border-bottom-width', 'outline', 'border-bottom-right-radius', 'border-right-width', 'border-top-width', 'font-style', 'text-transform', 'border-bottom-left-radius', 'border-left-width', 'border-spacing', 'border-style', 'border-top-right-radius', 'text-shadow', 'border-image', 'overflow-y', 'table-layout', 'background-size', 'behavior', 'body', 'name', 'letter-spacing', 'background-clip', 'pointer-events', 'transform', 'counter-reset', ]

# __all__ = [
#     'extract',
# ]

STATIC_ABBR = dict([
    ('b', 'bottom'), # Sides consistency
    ('ba', 'background'), # Instead of background-attachment
    ('bg', 'background'), # Instead of background: linear-gradient
    ('bd', 'border'), # Instead of border-style: dashed;
    ('bbc', 'border-bottom-color'), # Instead of background-break continuous
    ('br', 'border-right'), # Instead of border-radius
    ('bt', 'border-top'), # Instead of border: thick
    ('bdr', 'border-right'), # Instead of border-radius
    ('bds', 'border-style'), # Instead of border-spacing
    ('bo', 'border'), # Instead of background-origin
    ('bos', 'border-style'), # Instead of box-shadow (?)
    ('ct', 'content'), # Istead of color transparent
    ('f', 'font'), # Istead of float (do we really need this?)
    ('p', 'padding'), # Instead of position (w/h/p/m consistency)
    ('pr', 'padding-right'), # Instead of position relative
])

PAIRS = dict([
    ('bg', 'background'), # Instead of border-style: groove;
    ('bd', 'border'), # Instead of background (Zen CSS support)
    ('pg', 'page'),
    ('lt', 'letter'),
    ('tf', 'transform'),
    ('tr', 'transition'),
])

def get_all_properties():
    all_properties = list(get_css_dict().keys())

    # раширить парами "свойство значение" (например "position absolute")
    for prop_name in all_properties:
        property_values = css_flat_list(prop_name, get_css_dict())
        extends_sieve = (i for i in property_values if not i[1].startswith('<'))
        unit_sieve = (i for i in extends_sieve if not i[1].startswith('.'))
        all_properties.extend('{0} {1}'.format(prop_name, v[1]) for v in unit_sieve)
    return all_properties


def score(a, b):
    """Оценочная функция"""
    s = 0

    # увеличивает вес свойству со значением (они разделены пробелом)
    if a and ' ' == a[-1]:
        s += 3.0

    # уменьшить, если буква находится не на грницах слова
    if '-' in a[1:-1] or '-' in b[1:-1]:
        s += -2.0

    # уменьшить, если буква находится не на грницах слова
    if ' ' in a[1:-1] or ' ' in b[1:-1]:
        s += -0.5

    # если буква в начале слова после -
    if a and a[-1] == '-':
        s += 1.05

    # если буквы подряд
    if len(a) == 1:
        s += 1.0

    return s

def string_score(arr):
    """Получает оценку разбиения"""
    # s = sum(score(arr[i-1], arr[i]) for i in range(1, len(arr)))
    # if s >0 :
    #     print arr, s
    return sum(score(arr[i-1], arr[i]) for i in range(1, len(arr)))

def tree(css_property, abbr):
    # функция генерирует деревья (разбиения) из строки
    # (abvbc, abc) -> [[a, bvb ,c], [avb, b, c]]
    # print '\n', css_property
    if len(css_property) < len(abbr):
        return set([])
    trees = [[css_property[0], css_property[1:],],]
    for level in range(1, len(abbr)):
        # print level, trees
        for tr in trees:
            if level == 1 and len(trees) == 1:
                trees = []
            # находит индексы букв
            indexes = []
            i = -1
            try:
                while True:
                    i = tr[-1].index(abbr[level], i+1)
                    indexes.append(i)
            except ValueError:
                pass
            # print 'indexes len', len(indexes)
            for ind in indexes:
                if level == 1:
                    car = tr[:-1]
                    cdr = tr[-1]
                    first = cdr[:ind]
                    second = cdr[ind:]
                    add = []
                    add.append(car[-1] + first)
                    add.append(second)
                    # print '\t', car, '|', cdr,'|', first,'|', second, '-', add, level, '=', tr
                    trees.append(add)
                else:
                    car = tr[:-1]
                    cdr = tr[-1]
                    first = cdr[:ind]
                    second = cdr[ind:]
                    add = car
                    add.append(first)
                    add.append(second)
                    # print '\t', car, '|', cdr,'|', first,'|', second, '-', add, level, '=', tr
                    # print repr(first)
                    trees.append(add)
                # break
            trees_i = set([tuple(t) for t in trees if len(t) == level+1])
            trees = [list(t) for t in trees_i]
            # print 'trees_i', trees_i
            # break
            # print
        # break

    # удалить разбиения с двумя "-" в шилде
    ret = set([tuple(t) for t in trees])
    filtered = []
    for s in ret: # каждое элемент в сете
        for t in s: # каждый шилд в элементе
            # print '\t', t
            if t.count('-') > 1:
                break
        else:
            filtered.append(s)
    # print set([tuple(t) for t in trees])
    # print filtered
    return filtered


def prop_value(s1, val):
    """Генератор возвращает свойства и значения разделённые пробелом
    Из всех свойств выбирает только с совпадающим порядком букв"""
    for pv in get_all_properties():
        if ' ' not in pv.strip():
            continue
        prop, value = pv.split()
        if sub_string(value, val):
            if sub_string(prop, s1):
                yield '{0} {1}'.format(prop, value).strip()

def sub_string(string, sub):
    """Функция проверяет, следуют ли буквы в нужном порядке в слове"""
    index = 0
    for c in sub:
        try:
            index += string[index:].index(c)+1
        except ValueError:
            return False
    else:
        return True

def segmentation(abbr):
    """Разбивает абрревиатуру на элементы"""

    # Части аббревиатуры
    parts = {
        'abbr': abbr # todo: выкинуть, используется только в тестах
    }

    # Проверка на important свойство
    if '!' == abbr[-1]:
        abbr = abbr[:-1]
        parts['important'] = True
    else:
        parts['important'] = False

    # TODO: вынести regex в compile
    # todo: начать тестировать regex
    m = re.search(r'^([a-z]?[a-z-]*[a-z]).*$', abbr)
    property_ = m if m is None else m.group(1)
    if property_ is None:
        # Аббревиатура не найдена
        return parts
    # del m

    parts['property-value'] = property_

    # удалить из аббревиатуры property
    abbr = abbr[len(property_):]

    if abbr:
        parts['property-name'] = property_
        del parts['property-value']

    # убрать zen-style разделитель
    if abbr and ':' == abbr[0]:
        abbr = abbr[1:]

    if not abbr:
        return parts

    parts.update(value_parser(abbr))

    if 'value' in parts:
        assert parts['value'] is None
        del parts['value']
    elif ('type-value' not in parts and 'type-name' not in parts):
        parts['keyword-value'] = abbr

    # TODO: сохранять принимаемые значения, например parts['allow'] = ['<color_values>']
    return parts

def value_parser(abbr):
    # todo: поддержка аббревиатур "w-.e" то есть "width -|em"
    parts = {}

    # Checking the color
    # Better to replace with regex to simplify it
    dot_index = 0
    if '.' in abbr:
        dot_index = abbr.index('.')
    if abbr[0] == '#':
        parts['color'] = (abbr[1:dot_index or 99])
        if dot_index:
            parts['color_alpha'] = (abbr[dot_index:])
        parts['value'] = None
    try:
        if all((c.isupper() or c.isdigit() or c == '.') for c in abbr) and 0 <= int(abbr[:dot_index or 99], 16) <= 0xFFFFFF:
            parts['color'] = abbr[:dot_index or 99]
            if dot_index:
                parts['color_alpha'] = (abbr[dot_index:])
            parts['value'] = None
    except ValueError:
        pass

    # Проверка на цифровое значение
    val = None

    numbers = re.sub("[a-z%]+$", "", abbr)
    try:
        val = float(numbers)
        val = int(numbers)
    except ValueError:
        pass

    if val is not None:
        parts['type-value'] = val
        if abbr != numbers:
            parts['type-name'] = abbr[len(numbers):]

    return parts

def extract(s1):
    """В зависимости от найденных компонент в аббревиатуре применяет функцию extract"""
    # print repr(s1)
    prop_iter = []
    parts = segmentation(s1)
    abbr_value = False
    if 'property-name' in parts:
        if parts['important']:
            s1 = s1[:-1]
        if s1[-1] != ':' and s1 != parts['property-name']:
            abbr_value = True

    if 'color' in parts:
        prop_iter.extend(prop for prop, val in get_flat_css() if val == '<color_values>')

    if isinstance(parts.get('type-value'), int):
        prop_iter.extend(prop for prop, val in get_flat_css() if val == '<integer>')

    if isinstance(parts.get('type-value'), float):
        # TODO: добавить deg, grad, time
        prop_iter.extend(prop for prop, val in get_flat_css() if val in ('<length>', '<number>', 'percentage'))

    if 'keyword-value' in parts and not parts['keyword-value']:
        prop_iter.extend(get_all_properties())

    if 'keyword-value' in parts:
        prop_iter.extend(prop_value(parts['property-name'], parts['keyword-value']))
    elif 'color' not in parts or 'type-value' in parts:
        prop_iter.extend(get_all_properties())

    assert parts.get('property-name', '') or parts.get('property-value', '')
    abbr = ' '.join([
        parts.get('property-name', '') or parts.get('property-value', ''),
        parts.get('keyword-value', ''),
    ])

    # предустановленные правила
    abbr = abbr.strip()
    if abbr in STATIC_ABBR:
        property_ = STATIC_ABBR[abbr]
    else:
        starts_properties = []
        # todo: переделать механизм PAIRS
        # надо вынести константы в css-dict
        # по две буквы (bd, bg, ba)
        pair = PAIRS.get(abbr[:2], None)
        if pair is not None:
            starts_properties = [prop for prop in prop_iter if prop.startswith(pair) and sub_string(prop, abbr)]
        if not starts_properties:
            starts_properties = [prop for prop in prop_iter if prop[0] == abbr[0] and sub_string(prop, abbr)]

        if 'type-value' in parts:
            starts_properties = [i for i in starts_properties if ' ' not in i]

        property_ = hayaku_extract(abbr, starts_properties, PRIORITY_PROPERTIES, string_score)

    property_, value = property_.split(' ') if ' ' in property_ else (property_, None)
    # print property_, value
    if not property_:
        return {}

    parts['property-name'] = property_

    if value is not None:
        parts['keyword-value'] = value

    # Проверка соответствия свойства и значения

    allow_values = [val for prop, val in get_flat_css() if prop == parts['property-name']]

    if 'color' in parts and '<color_values>' not in allow_values:
        del parts['color']
    if 'type-value' in parts and not any((t in allow_values) for t in ['<integer>', 'percentage', '<length>', '<number>', '<alphavalue>']):
        del parts['type-value']
    if 'keyword-value' in parts and parts['keyword-value'] not in allow_values:
        del parts['keyword-value']

    if all([
            'keyword-value' not in parts,
            'type-value' not in parts,
            'color' not in parts,
        ]) and abbr_value:
        return {}

    # Добавить значение по-умолчанию
    if parts['property-name'] in get_css_dict():
        default_value = css_defaults(parts['property-name'], get_css_dict())
        if default_value is not None:
            parts['default-value'] = default_value
        obj = get_css_dict()[parts['property-name']]
        if 'prefixes' in obj:
            parts['prefixes'] = obj['prefixes']
            if 'no-unprefixed-property' in obj:
                parts['no-unprefixed-property'] = obj['no-unprefixed-property']

    if parts['abbr'] == parts.get('property-value'):
        del parts['property-value']

    return parts

def hayaku_extract(abbr, filtered, priority=None, score_func=None):
    # выбирает только те правила куда входят все буквы в нужном порядке

    #  все возможные разбиения
    trees_filtered = []
    for property_ in filtered:
        trees_filtered.extend(tree(property_, abbr))

    # оценки к разбиениям
    if score_func is not None:
        scores = [(score_func(i), i) for i in trees_filtered]

        # выбрать с максимальной оценкой
        if scores:
            max_score = max(s[0] for s in scores)
            filtered_scores = (i for s, i in scores if s == max_score)
            filtered = [''.join(t) for t in filtered_scores]
            if len(filtered) == 1:
                return ''.join(filtered[0])

    # выбрать более приоритетные
    if len(filtered) == 1:
        return filtered[0]
    elif len(filtered) > 1 and priority is not None:
        # выбирает по приоритету
        prior = []
        for f in filtered:
            p = f.split(' ')[0] if ' ' in f else f
            try:
                prior.append((priority.index(p), f))
            except ValueError:
                prior.append((len(priority)+1, f))
        prior.sort()
        try:
            return prior[0][1]
        except IndexError:
            return ''
    else:
        return ''
