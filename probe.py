# -*- coding: utf-8 -*-
# /*_*/

from ololo import (PROPS_DICT, PRIORITY_PROPERTIES, ALL_PROPERTIES)

__all__ = [
    'extract',
]

STATIC_ABBR = dict([
    ('b', 'bottom'), # Sides consistency
    ('ba', 'background'), # Instead of background-attachment
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
])

PAIRS = dict([
    ('bd', 'border'), # Instead of background (Zen CSS support)
    ('pg', 'page'),
    ('lt', 'letter'),
    ('tf', 'transform'),
])


pro_v = list(ALL_PROPERTIES)
for prop_name in PROPS_DICT:
    pro_v.extend('{0} {1}'.format(prop_name, v) for v in PROPS_DICT[prop_name][0])

# print ALL_PROPERTIES
# print len(ALL_PROPERTIES)

def score(a, b):
    """Оценочная функция"""
    s = 0
 
    # увеличивает вес свойству со значением (они разделены пробелом)   
    if a and ' ' in a[-1]:
        s += 1.5

    # уменьшить, если буква находится не на грницах слова
    if '-' in a[1:-1] or '-' in b[1:-1]:
        s += -1.5
    
    # если буква в начале слова после -
    if a and a[-1] == '-':
        s += 1.05

    # если буквы подряд
    if len(a) == 1:
        s += 1.0

    return s

def string_score(arr):
    """Получает оценку разбиения"""
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
        if ' ' not in pv:
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
    """Разбивает абрревиатуру на части"""
    # w1! -> ('w', 1, True)
    # pos:a -> ('pos', 'a', False)
    value = None
    important = abbr[-1] == '!'
    separator = abbr.find(':')
    if separator < 0:
        for i, c in enumerate(abbr):
            if c == '.' or c.isdigit():
                separator = i
                if abbr[i-1] == '-':
                    separator = i-1
                break
    if separator >= 0:
        property_ = abbr[:separator]
        if important:
            value = abbr[separator+1:-1]
        else:
            value = abbr[separator+1:]
    else:
        if important:
            property_ = abbr[:-1]
        else:
            property_ = abbr
    # есть ли цифры в value?
    if value is not None:
        num_val = bool(sum(c.isdigit() for c in value))
    else:
        num_val = False
    return property_, value, num_val, important

def extract(s1):
    """В зависимости от найденных компонент в аббревиатуре применяет функцию extract"""
    # print repr(s1)
    property_, value, num_val, important = segmentation(s1)
    # print s1, '|', property_, value, num_val
    if num_val:
        # print property_ , 'num'
        property_ = hayaku_extract(property_)
    else:
        # print property_, value, 'ok'
        property_ = hayaku_extract(property_, value)
    if ' ' in property_:
        property_, value = property_.split(' ')
    return property_, value, num_val, important

def hayaku_extract(abbr, value=None):
    # предустановленные правила
    if len(abbr) == 1 and (value is None or not value) and abbr in STATIC_ABBR:
        return STATIC_ABBR[abbr]
    # ограничить возможные варианты
    if value is None:
        prop_iter = pro_v
    elif value:
        prop_iter = prop_value(abbr, value)
        abbr = '{0}{1}'.format(abbr, value)
    else:
        prop_iter = ALL_PROPERTIES

    # по две буквы (bd, bg, ba)
    pair = PAIRS.get(abbr[:2], None)
    if pair is None:
        starts_properties = (prop for prop in prop_iter if prop[0] == abbr[0])
    else:
        starts_properties = (prop for prop in prop_iter if prop.startswith(pair))

    # выбирает только те правила куда входят все буквы в нужном порядке
    # TODO: заменить на генератор
    filtered  = [prop for prop in starts_properties if sub_string(prop, abbr)]

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
        filtered_scores = (s[1] for s in scores if s[0] == max_score)
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
            if ' 'in f:
                p, v = f.split(' ')
                try:
                    prior.append((PRIORITY_PROPERTIES.index(p), f))
                except ValueError:
                    prior.append((len(PRIORITY_PROPERTIES)+1, f))
            else:                
                try:
                    prior.append((PRIORITY_PROPERTIES.index(f), f))
                except ValueError:
                    prior.append((len(PRIORITY_PROPERTIES)+1, f))
        prior.sort()
        try:
            return prior[0][1]
        except IndexError:
            return ''
    else:
        return ''
