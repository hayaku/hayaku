# -*- coding: utf-8 -*-
# /*_*/

from ololo import PROPS_DICT

__all__ = [
    'extract',
]

STATIC_ABBR = dict([
    ('z', 'z-index'),
    ('w', 'width'),
    ('t', 'top'),
    ('r', 'right'),
    ('l', 'left'),
    ('b', 'bottom'),
    ('m', 'margin'),
    ('p', 'padding'),
    ('h', 'height'),
    ('q', 'quotes'),
    ('f', 'font'),
    ('d', 'display'),
    ('v', 'visibility'),
])

PAIRS = dict([
    ('bd', 'border'),
    ('bg', 'background'),
    ('ov', 'overflow'),
    ('fl', 'float'),
    ('pg', 'page'),

    ('lt', 'letter'),
    ('tf', 'transform'),
])

PRIORITY = ['display', 'color', 'margin', 'position', 'padding', 'width', 'background', 'zoom', 'height', 'top', 'vertical-align', 'overflow', 'left', 'margin-right', 'float', 'margin-left', 'cursor', 'text-decoration', 'font-size', 'margin-top', 'border', 'background-position', 'font', 'margin-bottom', 'padding-left', 'right', 'padding-right', 'line-height', 'white-space', 'text-align', 'border-color', 'padding-top', 'z-index', 'border-bottom', 'visibility', 'border-radius', 'padding-bottom', 'font-weight', 'clear', 'max-width', 'border-top', 'border-width', 'content', 'bottom', 'background-color', 'opacity', 'background-image', 'box-shadow', 'border-collapse', 'text-overflow', 'filter', 'border-right', 'text-indent', 'clip', 'min-width', 'min-height', 'border-left', 'max-height', 'border-right-color', 'border-top-color', 'transition', 'resize', 'overflow-x', 'list-style', 'word-wrap', 'border-left-color', 'word-spacing', 'background-repeat', 'user-select', 'border-bottom-color', 'box-sizing', 'border-top-left-radius', 'font-family', 'border-bottom-width', 'outline', 'border-bottom-right-radius', 'border-right-width', 'border-top-width', 'font-style', 'text-transform', 'border-bottom-left-radius', 'border-left-width', 'border-spacing', 'border-style', 'border-top-right-radius', 'text-shadow', 'border-image', 'overflow-y', 'table-layout', 'background-size', 'behavior', 'body', 'name', 'letter-spacing', 'background-clip', 'pointer-events', 'transform', 'counter-reset']

# содержит названия всех свойств css
pro = ['counter-reset', 'flex-direction', 'counter-increment', 'min-height', 'quotes', 'border-top', 'nav-right', 'font', 'white-space-collapse', 'background-size', 'list-style-image', 'background-origin', 'flex-align', 'text-emphasis-position', 'font-stretch', 'outline-width', 'border-length', 'border-right', 'columns', 'border-radius', 'border-bottom-image', 'box-shadow', 'border-corner-image', 'column-rule', 'border-top-right-radius', 'word-wrap', 'text-emphasis-color', 'border-bottom', 'border-spacing', 'max-zoom', 'column-rule-width', 'background', 'list-style-type', 'nav-left', 'text-align', 'border-image-slice', 'name', 'overflow-style', 'page-break-inside', 'orphans', 'page-break-before', 'zoom', 'break-after', 'column-span', 'border-fit', 'column-fill', 'tab-size', 'border-bottom-color', 'border-bottom-right-radius', 'line-height', 'padding-left', 'text-align-last', 'font-size', 'right', 'transform', 'outline-color', 'break-inside', 'border-top-right-image', 'text-outline', 'word-spacing', 'list-style-position', 'padding-top', 'border-image-repeat', 'border-top-width', 'bottom', 'content', 'border-right-style', 'padding-right', 'border-left-style', 'background-color', 'column-gap', 'body', 'border-left-image', 'text-emphasis', 'border-right-image', 'background-break', 'animation-delay', 'unicode-bidi', 'text-shadow', 'border-image', 'max-width', 'font-family', 'caption-side', 'animation-duration', 'font-emphasize', 'font-smooth', 'text-transform', 'transition', 'filter', 'pointer-events', 'border-right-width', 'border-image-width', 'column-rule-color', 'border-top-style', 'text-replace', 'opacity', 'text-justify', 'color', 'border-collapse', 'border-bottom-width', 'float', 'text-height', 'height', 'max-height', 'outline-offset', 'margin-right', 'outline-style', 'background-clip', 'border-bottom-left-radius', 'text-emphasis-style', 'top', 'border-width', 'min-width', 'width', 'font-variant', 'border-break', 'border-top-color', 'background-position', 'flex-pack', 'empty-cells', 'direction', 'border-left', 'animation-play-state', 'visibility', 'transition-delay', 'padding', 'z-index', 'background-position-y', 'text-overflow-mode', 'background-attachment', 'overflow', 'user-select', 'resize', 'outline', 'font-emphasize-style', 'column-count', 'user-zoom', 'font-size-adjust', 'font-emphasize-position', 'cursor', 'column-rule-style', 'behavior', 'animation-direction', 'margin', 'display', 'border-left-width', 'letter-spacing', 'border-top-left-radius', 'vertical-align', 'orientation', 'clip', 'border-color', 'column-width', 'list-style', 'margin-left', 'transform-origin', 'nav-down', 'padding-bottom', 'animation-name', 'border-bottom-right-image', 'widows', 'border', 'font-style', 'text-overflow-ellipsis', 'border-left-color', 'border-bottom-left-image', 'break-before', 'overflow-y', 'overflow-x', 'word-break', 'background-repeat', 'table-layout', 'text-overflow', 'margin-bottom', 'font-effect', 'nav-up', 'animation', 'border-top-left-image', 'border-image-outset', 'font-weight', 'text-wrap', 'box-decoration-break', 'border-right-color', 'min-zoom', 'page-break-after', 'transition-property', 'text-decoration', 'white-space', 'text-indent', 'nav-index', 'background-image', 'flex-order', 'border-bottom-style', 'clear', 'animation-timing-function', 'border-top-image', 'border-style', 'background-position-x', 'border-image-source', 'box-sizing', 'transition-duration', 'margin-top', 'animation-iteration-count', 'hyphens', 'position', 'transition-timing-function', 'left']


pro_v = list(pro)
for prop_name in PROPS_DICT:
    pro_v.extend('{0} {1}'.format(prop_name, v) for v in PROPS_DICT[prop_name][0])

# print pro
# print len(pro)

def score(a, b):
    """Оценочная функция"""
    s = 0
    # print a,b 
    if a and ' ' in a[-1]:
        s += 1.5

    if '-' in a[1:-1] or '-' in b[1:-1]:
        s += -1.5

    if a and a[-1] == '-':
        s += 1.05

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
    for pv in pro_v:
        if ' ' not in pv:
            continue
        prop, value = pv.split()
        if sub_string(value, val):
            if sub_string(prop, s1):
                yield '{0} {1}'.format(prop, value)

def sub_string(string, sub):
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
    value = ''
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
    num_val = bool(sum(c.isdigit() for c in value))
    return property_, value, num_val, important

def extract(s1):
    # разобрать аббревиатуру
    property_, value, num_val, important = segmentation(s1)
    # print property_, num_val
    if num_val:
        # print property_ , 'num'
        property_ = hayaku_extract(property_)
    else:
        # print property_, value, 'ok'
        property_ = hayaku_extract(property_, value)
    if ' ' in property_:
        property_, value = property_.split(' ')
    return property_, value, num_val, important

def hayaku_extract(s1, val=''):
    # предустановленные правила
    if s1 in STATIC_ABBR and not val:
        return STATIC_ABBR[s1]

    if val:
        pro_i = prop_value(s1, val)
        s1 = '{0}{1}'.format(s1, val)
    else:
        pro_i = pro_v

    # по две буквы
    pair = PAIRS.get(s1[:2], None)
    if pair is None:
        pro1 = (p for p in pro_i if p[0] == s1[0])
    else:
        pro1 = (p for p in pro_i if p.startswith(pair))

    # выбирает только те правила куда входят все буквы в нужном порядке
    # TODO: заменить на генератор
    filtered  = [p for p in pro1 if sub_string(p, s1)]

    #  все возможные разбиения
    trees_filtered = []
    for f in filtered:
        trees_filtered.extend(tree(f, s1))

    # print len(trees_filtered), trees_filtered
    
    # оценки к разбиениям
    scores = []
    for i in trees_filtered:
        add = (string_score(i), i)
        scores.append(add)
        # print add

    # выбрать с максимальной оценкой
    if scores:
        max_score = max(s[0] for s in scores)
        filtered_scores = [s[1] for s in scores if s[0] == max_score]
        # print filtered_scores
        filtered = [''.join(t) for t in filtered_scores]
        if len(filtered) == 1:
            return ''.join(filtered[0])

    # вывбрать более приоритетные
    # print filtered, s1
    if len(filtered) == 1:
        return filtered[0]
    elif len(filtered) > 1:
        # выбирает по приоритету
        prior = []
        for f in filtered:
            try:
                prior.append((PRIORITY.index(f), f))
            except ValueError:
                prior.append((len(PRIORITY)+1, f))
        prior.sort()
        try:
            return prior[0][1]
        except IndexError:
            return ''
    else:
        return ''
        