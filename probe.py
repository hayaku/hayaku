# -*- coding: utf-8 -*-
# /*_*/
import re

from ololo import (PRIORITY_PROPERTIES, ALL_PROPERTIES)
from css_dict_driver import props_dict, flat_css_dict

PROPS_DICT = props_dict()

__all__ = [
    'extract',
]

STATIC_ABBR = dict([
    ('b', 'bottom'), # Sides consistency
    ('ba', 'background'), # Instead of background-attachment
    ('bd', 'border'), # Instead of border-style: dashed;
    ('bbc', 'border-bottom-color'), # Instead of background-break continuous
    ('br', 'border-right'), # Instead of border-radius
    ('bdr', 'border-right'), # Instead of border-radius
    ('bds', 'border-style'), # Instead of border-spacing
    ('bo', 'border'), # Instead of background-origin
    ('bos', 'border-style'), # Instead of box-shadow (?)
    ('ct', 'content'), # Istead of color transparent
    ('f', 'font'), # Istead of float (do we really need this?)
    ('p', 'padding'), # Instead of position (w/h/p/m consistency)
    ('pr', 'padding-right'), # Instead of position relative
    ('lsn', 'list-style: none'),
])

PAIRS = dict([
    ('bg', 'background'), # Instead of border-style: groove;
    ('bd', 'border'), # Instead of background (Zen CSS support)
    ('pg', 'page'),
    ('lt', 'letter'),
    ('tf', 'transform'),
    ('tr', 'transition'),
])

# названия всех свойств
pro_v = list(ALL_PROPERTIES)

# раширить парами "свойство значение" (например "position absolute")
for prop_name in PROPS_DICT:
    pro_v.extend('{0} {1}'.format(prop_name, v) for v in PROPS_DICT[prop_name][0])

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
    for pv in pro_v:
        if ' ' not in pv.strip():
            continue
        prop, value = pv.split()
        if sub_string(value, val):
            if sub_string(prop, s1):
                yield '{0} {1}'.format(prop, value)

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
        'abbr': abbr
    }

    # Проверка на important свойство
    if '!' == abbr[-1]:
        abbr = abbr[:-1]
        parts['important'] = True
    else:
        parts['important'] = False

    # TODO: вынести regex в compile
    m = re.search(r'^([a-z]?[a-z-]*[a-z]).*$', abbr)
    property_ = m if m is None else m.group(1)
    if property_ is None:
        # Аббревиатура не найдена
        return parts
    # del m

    parts['property'] = property_

    # Разделить на части ":"
    abbr = abbr[len(property_):]

    if abbr and ':' == abbr[0]:
        abbr = abbr[1:]

    if not abbr:
        return parts

    if abbr:
        parts.update(value_parser(abbr))

    if 'num' not in parts:
        parts['value'] = abbr

    return parts

def value_parser(abbr):
    parts = {}

    # Проверка на цвет
    if abbr[0] == '#':
        parts['color'] = abbr[1:]

    #if abbr[0].isalpha() or abbr[0].isupper():
    if all(abb.lower() in ('a', 'b', 'c', 'd', 'e', 'f') for abb in abbr):
        parts['color'] = abbr

    # Проверка на цифровое значение
    val = None
    try:
        val = float(abbr)
        val = int(abbr)
    except ValueError:
        pass

    if val is not None:
        parts['num'] = val

    return parts

def extract(s1):
    """В зависимости от найденных компонент в аббревиатуре применяет функцию extract"""
    # print repr(s1)
    css_properties = []
    parts = segmentation(s1)

    if 'color' in parts:
        css_properties.extend(prop for prop, val in flat_css_dict() if val == '<color>')

    if 'num' in parts and isinstance(parts['num'], int):
        css_properties.extend(prop for prop, val in flat_css_dict() if val == '<integer>')

    if 'num' in parts and isinstance(parts['num'], float):
        # TODO: добавить deg, grad, time
        css_properties.extend(prop for prop, val in flat_css_dict() if val in ('<length>', 'percentage'))

    prop_iter = []

    if css_properties:
        prop_iter.extend(css_properties)

    if 'value' in parts and parts['value'] == '':
        prop_iter.extend(ALL_PROPERTIES)
    if 'value' in parts:
        prop_iter.extend(prop_value(parts['property'], parts['value']))
    else:
        prop_iter.extend(pro_v)

    abbr = '{0} {1}'.format(parts['property'], parts.get('value', ''))
    property_ = hayaku_extract(abbr.strip(), prop_iter)

    value = None
    if ' ' in property_:
        property_, value = property_.split(' ')

    if value is not None:
        parts['value_extracted'] = value
    parts['property_extracted'] = property_
    return parts

def hayaku_extract(abbr, prop_iter):
    # предустановленные правила
    if abbr in STATIC_ABBR:
        return STATIC_ABBR[abbr]

    starts_properties = []

    # todo: переделать механизм PAIRS
    # надо вынести константы в css-dict

    # по две буквы (bd, bg, ba)
    pair = PAIRS.get(abbr[:2], None)
    if pair is not None:
        starts_properties = [prop for prop in prop_iter if prop.startswith(pair) and sub_string(prop, abbr)]

    if not starts_properties:
        starts_properties = [prop for prop in prop_iter if prop[0] == abbr[0] and sub_string(prop, abbr)]

    # выбирает только те правила куда входят все буквы в нужном порядке
    # TODO: заменить на генератор
    # filtered  = [prop for prop in starts_properties if sub_string(prop, abbr)]
    filtered = starts_properties

    #  все возможные разбиения
    trees_filtered = []
    for property_ in filtered:
        trees_filtered.extend(tree(property_, abbr))

    # print len(trees_filtered), trees_filtered

    # оценки к разбиениям
    scores = [(string_score(i), i) for i in trees_filtered]
    # for i in trees_filtered:
    #     add = (string_score(i), i)
    #     scores.append(add)
        # print add

    # выбрать с максимальной оценкой
    if scores:
        max_score = max(s[0] for s in scores)
        filtered_scores = (i for s, i in scores if s == max_score)
        filtered = [''.join(t) for t in filtered_scores]
        if len(filtered) == 1:
            return ''.join(filtered[0])

    # вывбрать более приоритетные
    # print filtered, abbr
    if len(filtered) == 1:
        return filtered[0]
    elif len(filtered) > 1:
        # выбирает по приоритету
        prior = []
        for f in filtered:
            if ' ' in f:
                p, v = f.split(' ')
            else:
                p = f
            try:
                prior.append((PRIORITY_PROPERTIES.index(p), f))
            except ValueError:
                prior.append((len(PRIORITY_PROPERTIES)+1, f))
        prior.sort()
        try:
            return prior[0][1]
        except IndexError:
            return ''
    else:
        return ''
