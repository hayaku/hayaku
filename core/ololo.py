# -*- coding: utf-8 -*-
# /*_*/

COMMONS = {
  'overflow' :
  [
    'scroll',
    'visible',
    'hidden',
    'auto'
  ],
  'borderstyle' :
  [
    'solid',
    'none',
    'dashed',
    'dotted',
    'double',
    'dot-dash',
    'dot-dot-dash',
    'hidden',
    'groove',
    'ridge',
    'inset',
    'outset',
    'wave'
  ],
  'lengths' :
  [
    'px',
    'em',
    'ex',
    'rem',
    '%',
    'in',
    'cm',
    'mm',
    'pt',
    'pc'
  ],
  'prefixes' :
  [
    '-webkit-',
    '   -moz-',
    '     -o-',
    '        ' # need to find a better way to do all these prefix stuff
  ],
  'prefixes-bra' :
  [
    '-webkit-',
    '   -moz-',
    '        ' # need to find a better way to do all these prefix stuff
  ],
  'colors' :
  [
    'transparent',
    'red',
    'black',
    'white',
  ]
  
}

PROPS = [
  {
    'name' : 'margin-top',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'margin-right',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'margin-bottom',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'margin-left',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'margin',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'padding',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'padding-top',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'padding-right',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'padding-bottom',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'padding-left',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'position',
    'values' :
    [
      'static',
      'relative',
      'absolute',
      'fixed',
    ]
  },
  {
    'name' : 'top',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'right',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'bottom',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'left',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'z-index',
    'values' : ['auto']
  },
  {
    'name' : 'float',
    'values' :
    [
      'left',
      'right',
      'none',
    ]
  },
  {
    'name' : 'clear',
    'values' :
    [
      'left',
      'right',
      'both',
      'none',
    ]
  },
  {
    'name' : 'display',
    'values' :
    [
      'inline',
      'block',
      'list-item',
      'run-in',
      'inline-block',
      'compact',
      'table',
      'inline-table',
      'table-row',
      'table-cell',
      'table-row-group',
      'table-header-group',
      'table-footer-group',
      'table-column',
      'table-column-group',
      'table-caption',
      'none',
    ]
  },
  {
    'name' : 'visibility',
    'values' :
    [
      'visible',
      'hidden',
      'collapse'
    ]   
    
  },
  {
    'name' : 'overflow',
    'values' : COMMONS['overflow']
  },
  {
    'name' : 'overflow-x',
    'values' : COMMONS['overflow']
  },
  {
    'name' : 'overflow-y',
    'values' : COMMONS['overflow']
  },
  {
    'name' : 'overflow-style',
    'values' :
    [
      'auto',
      'scrollbar',
      'panner',
      'move',
      'marquee',
    ]
  },
  {
    'name' : 'zoom',
    'units' : [''],
    'default' : '1'
  },
  {
    'name' : 'clip',
    'values' :
    [
      'rect(0 0 0 0)',
      'auto'
    ]
  },
  {
    'name' : 'width',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'height',
    'values' :
    [
      'auto',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'max-width',
    'values' :
    [
      'none',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'max-height',
    'values' :
    [
      'none',
    ],
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'min-width',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'min-height',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'outline',
    'values' :
    [
      'none',
    ]
  },
  {
    'name' : 'outline-offset',
  },
  {
    'name' : 'outline-width',
  },
  {
    'name' : 'outline-style',
  },
  {
    'name' : 'outline-color',
  },
  {
    'name' : 'border',
    'units' :
    [
      'px solid ${|:#000}',
    ]
  },
  {
    'name' : 'border-top',
  },
  {
    'name' : 'border-right',
  },
  {
    'name' : 'border-bottom',
  },
  {
    'name' : 'border-left',
  },
  {
    'name' : 'border-color',
  },
  {
    'name' : 'border-style',
    'values' : COMMONS['borderstyle']
  },
  {
    'name' : 'border-width',
  },
  {
    'name' : 'border-break',
    'values' :
    [
      'close'
    ]
  },
  {
    'name' : 'border-collapse',
    'values' :
    [
      'collapse',
      'separate'
    ]
  },
  {
    'name' : 'border-image',
  },
  {
    'name' : 'border-fit',
    'values' :
    [
      'clip',
      'repeat',
      'scale',
      'stretch',
      'overwrite',
      'overflow',
      'space'
    ]
  },
  {
    'name' : 'border-length',
    'values' :
    [
      'auto'
    ]
  },
  {
    'name' : 'border-spacing',
  },
  {
    'name' : 'border-radius',
    'units' : COMMONS['lengths'],
    'prefixes' : COMMONS['prefixes-bra']
  },
  {
    'name' : 'border-top-image',
  },
  {
    'name' : 'border-right-image',
  },
  {
    'name' : 'border-bottom-image',
  },
  {
    'name' : 'border-left-image',
  },
  {
    'name' : 'border-corner-image',
  },
  {
    'name' : 'border-top-left-image',
  },
  {
    'name' : 'border-top-right-image',
  },
  {
    'name' : 'border-bottom-right-image',
  },
  {
    'name' : 'border-bottom-left-image',
  },
  {
    'name' : 'border-top-width',
  },
  {
    'name' : 'border-top-style',
    'values' : COMMONS['borderstyle']
  },
  {
    'name' : 'border-top-color',
  },
  {
    'name' : 'border-right-width',
  },
  {
    'name' : 'border-right-style',
    'values' : COMMONS['borderstyle']
  },
  {
    'name' : 'border-right-color',
  },
  {
    'name' : 'border-bottom-width',
  },
  {
    'name' : 'border-bottom-style',
    'values' : COMMONS['borderstyle']
  },
  {
    'name' : 'border-bottom-color',
  },
  {
    'name' : 'border-left-width',
  },
  {
    'name' : 'border-left-style',
    'values' : COMMONS['borderstyle']
  },
  {
    'name' : 'border-left-color',
  },
  {
    'name' : 'border-top-right-radius',
  },
  {
    'name' : 'border-top-left-radius',
  },
  {
    'name' : 'border-bottom-right-radius',
  },
  {
    'name' : 'border-bottom-left-radius',
  },
  {
    'name' : 'background',
    'values' :
    [
      'none',
      'transparent'
    ]
  },
  {
    'name' : 'background-color',
    'values' :
    [
      'transparent'
    ]
  },
  {
    'name' : 'background-image',
    'values' :
    [
      'url()',
      'none'
    ]
  },
  {
    'name' : 'background-repeat',
    'values' :
    [
      'repeat',
      'repeat-x',
      'repeat-y',
      'no-repeat',
    ]
  },
  {
    'name' : 'background-attachment',
    'values' :
    [
      'fixed',
      'scroll',
    ]
  },
  {
    'name' : 'background-position',
    #'values' : COMMONS['repeats'] # no repeats in COMMONS
  },
  {
    'name' : 'background-position-x',
  },
  {
    'name' : 'background-position-y',
  },
  {
    'name' : 'background-break',
    'values' :
    [
      'bounding-box',
      'each-box',
      'continuous',
    ]
  },
  {
    'name' : 'background-clip',
    'values' :
    [
      'border-box',
      'padding-box',
      'content-box',
      'no-clip',
    ]
  },
  {
    'name' : 'background-origin',
    'values' :
    [
      'border-box',
      'padding-box',
      'content-box',
    ]
  },
  {
    'name' : 'background-size',
    'values' :
    [
      'auto',
      'contain',
      'cover',
    ]
  },
  {
    'name' : 'box-sizing',
    'values' :
    [
      'content-box',
      'border-box'
    ],
    'prefixes' :
    [
      '-webkit-',
      '   -moz-',
      '        ' # need to find a better way to do all these prefix stuff
    ],
    
  },
  {
    'name' : 'box-shadow',
    'prefixes' : COMMONS['prefixes'],
  },
  {
    'name' : 'color',
    'values' : COMMONS['colors'],
  },
  {
    'name' : 'table-layout',
    'values' :
    [
      'auto',
      'fixed'
    ]
  },
  {
    'name' : 'caption-side',
    'values' :
    [
      'top',
      'bottom'
    ]
  },
  {
    'name' : 'empty-cells',
    'values' :
    [
      'show',
      'hide'
    ]
  },
  {
    'name' : 'list-style',
    'values' :
    [
      'none'
    ]
  },
  {
    'name' : 'list-style-position',
    'values' :
    [
      'inside',
      'outside'
    ]
  },
  {
    'name' : 'list-style-type',
    'values' :
    [
      'none',
      'disc',
      'circle',
      'square',
      'decimal',
      'decimal-leading-zero',
      'lower-roman',
      'upper-roman',
    ]
  },
  {
    'name' : 'list-style-image',
    'values' :
    [
      'none'
    ]
  },
  {
    'name' : 'cursor',
    'values' :
    [
      'auto',
      'default',
      'crosshair',
      'hand',
      'help',
      'move',
      'pointer',
      'text',
    ]
  },
  {
    'name' : 'quotes',
    'values' :
    [
      'none'
    ]
  },
  {
    'name' : 'content',
    'values' :
    [
      'normal',
      'open-quote',
      'no-open-quote',
      'close-quote',
      'no-close-quote',
      'attr()',
      'counter()',
      'counters()',
    ]
  },
  {
    'name' : 'counter-increment',
  },
  {
    'name' : 'counter-reset',
  },
  {
    'name' : 'vertical-align',
    'values' :
    [
      'sub',
      'super',
      'top',
      'text-top',
      'middle',
      'bottom',
      'baseline',
      'text-bottom'
    ]
  },
  {
    'name' : 'text-align',
    'values' :
    [
      'left',
      'right',
      'center',
      'justify'
    ]
  },
  {
    'name' : 'text-align-last',
    'values' :
    [
      'left',
      'right',
      'center',
      'auto'
    ]
  },
  {
    'name' : 'text-decoration',
    'values' :
    [
      'none',
      'overline',
      'line-through',
      'underline'
    ]
    
  },
  {
    'name' : 'text-overflow',
    'values' :
    [
      'none',
      'ellipsis'
    ]
    
  },
  {
    'name' : 'text-emphasis',
    'values' :
    [
      'none',
      'before',
      'after',
      'accent',
      'dot',
      'circle',
      'disc',
    ]
  },
  {
    'name' : 'text-height',
    'values' :
    [
      'auto',
      'font-size',
      'text-size',
      'max-size'
    ]
  },
  {
    'name' : 'text-indent',
    'values' :
    [
      '-9999px',
    ]
  },
  {
    'name' : 'text-justify',
    'values' :
    [
      'auto',
      'inter-word',
      'inter-ideograph',
      'inter-cluster',
      'distribute',
      'kashida',
      'tibetan',
    ]
  },
  {
    'name' : 'text-outline',
    'values' :
    [
      'none',
    ]
  },
  {
    'name' : 'text-replace',
    'values' :
    [
      'none',
    ]
  },
  {
    'name' : 'text-transform',
    'values' :
    [
      'none',
      'uppercase',
      'capitalize',
      'lowercase',
    ]
  },
  {
    'name' : 'text-wrap',
    'values' :
    [
      'normal',
      'none',
      'unrestricted',
      'suppress',
    ]
  },
  {
    'name' : 'text-shadow',
    'values' :
    [
      'none',
    ],
  },
  {
    'name' : 'line-height',
    'units' : ['']+COMMONS['lengths'],
  },
  {
    'name' : 'white-space',
    'values' :
    [
      'normal',
      'nowrap',
      'pre',
      'pre-wrap',
      'pre-line',
    ]
  },
  {
    'name' : 'white-space-collapse',
    'values' :
    [
      'normal',
      'keep-all',
      'loose',
      'break-strict',
      'break-all',
    ]
  },
  {
    'name' : 'word-break',
    'values' :
    [
      'normal',
      'keep-all',
      'loose',
      'break-strict',
      'break-all',
    ]
  },
  {
    'name' : 'word-spacing',
  },
  {
    'name' : 'word-wrap',
    'values' :
    [
      'normal',
      'none',
      'unrestricted',
      'suppress',
    ]
  },
  {
    'name' : 'letter-spacing',
  },
  {
    'name' : 'font',
  },
  {
    'name' : 'font-size',
    'units' : COMMONS['lengths'],
  },
  {
    'name' : 'font-size-adjust',
  },
  {
    'name' : 'font-weight',
    'values' :
    [
      'normal',
      'bold',
      'bolder',
      'lighter',
    ]
  },
  {
    'name' : 'font-style',
    'values' :
    [
      'normal',
      'italic',
      'oblique',
    ]
  },
  {
    'name' : 'font-variant',
    'values' :
    [
      'normal',
      'small-caps',
    ]
  },
  {
    'name' : 'font-family',
    'values' :
    [
      'serif',
      'sans-serif',
      'monospace',
    ]
  },
  {
    'name' : 'font-effect',
    'values' :
    [
      'none',
      'engrave',
      'emboss',
      'outline',
    ]
  },
  {
    'name' : 'font-emphasize',
  },
  {
    'name' : 'font-emphasize-position',
    'values' :
    [
      'before',
      'after',
    ]
  },
  {
    'name' : 'font-emphasize-style',
    'values' :
    [
      'none',
      'accent',
      'dot',
      'circle',
      'disc',
    ]
  },
  {
    'name' : 'font-smooth',
    'values' :
    [
      'auto',
      'nover',
      'always',
    ]
  },
  {
    'name' : 'font-stretch',
    'values' :
    [
      'normal',
      'ultra-condensed',
      'extra-condensed',
      'condensed',
      'semi-condensed',
      'semi-expanded',
      'expanded',
      'extra-expanded',
      'ultra-expanded',
    ]
  },
  {
    'name' : 'opacity',
  },
  {
    'name' : 'resize',
    'values' :
    [
      'none',
      'both',
      'horizontal',
      'vertical',
    ]
  },
  {
    'name' : 'page-break-before',
    'values' :
    [
      'auto',
      'always',
      'left',
      'right',
    ]
  },
  {
    'name' : 'page-break-inside',
    'values' :
    [
      'auto',
      'avoid',
    ]
  },
  {
    'name' : 'page-break-after',
    'values' :
    [
      'auto',
      'always',
      'left',
      'right',
    ]
  },
  {
    'name' : 'orphans',
  },
  {
    'name' : 'widows',
  },
  {
    'name' : 'filter',
  },
  {
    'name' : 'transition',
    'values' :
    [
      'all .3s ease'
    ],
    'prefixes' : COMMONS['prefixes']
  },
  {
    'name' : 'transform',
    'values' :
    [
      'scale($|)',
      'skew($|deg)',
      'rotate($|deg)',
      'translate($|)'
    ],
    'prefixes' : COMMONS['prefixes']
  },
  {
    'name' : 'user-select',
    'values' :
    [
      'none',
      'auto',
      'text'
    ],
    'prefixes' : COMMONS['prefixes-bra']
  },
]

GLOBALSHORTCUTS = {
  'z:a' : ['z-index','auto'],
  'c' : ['color',''],
  'zoo' : ['zoom','1'],
  'fz' : ['font-size',''],
  'f' : ['font',''],
  'bxz' : ['box-sizing',''],
  'bo' : ['border','']
}

VALUESHORTCUTS = {
  'red' : '#f00',
  'black' : '#000',
  'white' : '#fff',
}

# Словарь свойств и значений
# Версия ссгенерированная из ololo
# TODO http://www.w3.org/TR/2011/REC-CSS2-20110607/propidx.html парсить спецификацию

# формат
# ключ = название свойства
# значение = кортеж из возможных свойств
PROPS_DICT = {
  # 'background': (['none', 'transparent'],),
  'background-attachment': (['fixed', 'scroll'],),
  'background-break': (['bounding-box', 'each-box', 'continuous'],),
  'background-clip': (['border-box', 'padding-box', 'content-box', 'no-clip'],),
  # 'background-color': (['transparent'],),
  # 'background-image': (['url()', 'none'],),
  'background-origin': (['border-box', 'padding-box', 'content-box'],),
  'background-repeat': (['repeat', 'repeat-x', 'repeat-y', 'no-repeat'],),
  'background-size': (['auto', 'contain', 'cover'],),
  'background': (['none'],),
  'border-bottom': (['none'],),
  'border-bottom-style': (['solid', 'none', 'dashed', 'dotted', 'double', 'dot-dash', 'dot-dot-dash', 'hidden', 'groove', 'ridge', 'inset', 'outset', 'wave'],),
  'border-break': (['close'],),
  'border-top-left-image': (['continue'],),
  'border-top-right-image': (['continue'],),
  'border-bottom-right-image': (['continue'],),
  'border-bottom-left-image': (['continue'],),
  'border-collapse': (['collapse', 'separate'],),
  'border-fit': (['clip', 'repeat', 'scale', 'stretch', 'overwrite', 'overflow', 'space'],),
  'border-left-style': (['solid', 'none', 'dashed', 'dotted', 'double', 'dot-dash', 'dot-dot-dash', 'hidden', 'groove', 'ridge', 'inset', 'outset', 'wave'],),
  'border-length': (['auto'],),
  'border-right-style': (['solid', 'none', 'dashed', 'dotted', 'double', 'dot-dash', 'dot-dot-dash', 'hidden', 'groove', 'ridge', 'inset', 'outset', 'wave'],),
  'border-style': (['solid', 'none', 'dashed', 'dotted', 'double', 'dot-dash', 'dot-dot-dash', 'hidden', 'groove', 'ridge', 'inset', 'outset', 'wave'],),
  'border-top-style': (['solid', 'none', 'dashed', 'dotted', 'double', 'dot-dash', 'dot-dot-dash', 'hidden', 'groove', 'ridge', 'inset', 'outset', 'wave'],),
  'box-sizing': (['content-box','border-box'],),
  'caption-side': (['top', 'bottom'],),
  'clear': (['left', 'right', 'both', 'none'],),
  # 'clip': (['rect(0 0 0 0)', 'auto'],),
  'color': (['transparent'],),
  'content': (['normal', 'open-quote', 'no-open-quote', 'close-quote', 'no-close-quote', 'attr()', 'counter()', 'counters()'],),
  'cursor': (['auto', 'default', 'crosshair', 'hand', 'help', 'move', 'pointer', 'text'],),
  'display': (['inline', 'block', 'list-item', 'run-in', 'inline-block', 'compact', 'table', 'inline-table', 'table-row', 'table-cell', 'table-row-group', 'table-header-group', 'table-footer-group', 'table-column', 'table-column-group', 'table-caption', 'none'],),
  'empty-cells': (['show', 'hide'],),
  'float': (['left', 'right', 'none'],),
  'font-effect': (['none', 'engrave', 'emboss', 'outline'],),
  'font-emphasize-position': (['before', 'after'],),
  'font-emphasize-style': (['none', 'accent', 'dot', 'circle', 'disc'],),
  'font-family': (['serif', 'sans-serif', 'monospace'],),
  'font-smooth': (['auto', 'nover', 'always'],),
  'font-stretch': (['normal', 'ultra-condensed', 'extra-condensed', 'condensed', 'semi-condensed', 'semi-expanded', 'expanded', 'extra-expanded', 'ultra-expanded'],),
  'font-style': (['normal', 'italic', 'oblique'],),
  'font-variant': (['normal', 'small-caps'],),
  'font-weight': (['normal', 'bold', 'bolder', 'lighter'],),
  'list-style': (['none'],),
  'list-style-image': (['none'],),
  'list-style-position': (['inside', 'outside'],),
  'list-style-type': (['none', 'disc', 'circle', 'square', 'decimal', 'decimal-leading-zero', 'lower-roman', 'upper-roman'],),
  'max-height': (['none'],),
  'max-width': (['none'],),
  'outline': (['none'],),
  'overflow': (['scroll', 'visible', 'hidden', 'auto'],),
  'overflow-style': (['auto', 'scrollbar', 'panner', 'move', 'marquee'],),
  'overflow-x': (['scroll', 'visible', 'hidden', 'auto'],),
  'overflow-y': (['scroll', 'visible', 'hidden', 'auto'],),
  'page-break-after': (['auto', 'always', 'left', 'right'],),
  'page-break-before': (['auto', 'always', 'left', 'right'],),
  'page-break-inside': (['auto', 'avoid'],),
  'position': (['static', 'relative', 'absolute', 'fixed'],),
  'quotes': (['none'],),
  'resize': (['none', 'both', 'horizontal', 'vertical'],),
  'table-layout': (['auto', 'fixed'],),
  'text-align': (['left', 'right', 'center', 'justify'],),
  'text-align-last': (['left', 'right', 'center', 'auto'],),
  'text-decoration': (['none', 'overline', 'line-through', 'underline'],),
  'text-emphasis': (['none', 'before', 'after', 'accent', 'dot', 'circle', 'disc'],),
  'text-height': (['auto', 'font-size', 'text-size', 'max-size'],),
  'text-indent': (['hanging', 'each-line'],),
  'text-justify': (['auto', 'inter-word', 'inter-ideograph', 'inter-cluster', 'distribute', 'kashida', 'tibetan'],),
  'text-outline': (['none'],),
  'text-overflow': (['none', 'ellipsis'],),
  'text-replace': (['none'],),
  'text-shadow': (['none'],),
  'text-transform': (['none', 'uppercase', 'capitalize', 'lowercase'],),
  'text-wrap': (['normal', 'none', 'unrestricted', 'suppress'],),
  'vertical-align': (['sub', 'super', 'top', 'text-top', 'middle', 'bottom', 'baseline', 'text-bottom'],),
  'visibility': (['visible', 'hidden', 'collapse'],),
  'white-space': (['normal', 'nowrap', 'pre', 'pre-wrap', 'pre-line'],),
  'white-space-collapse': (['normal', 'keep-all', 'loose', 'break-strict', 'break-all'],),
  'word-break': (['normal', 'keep-all', 'loose', 'break-strict', 'break-all'],),
  'word-wrap': (['normal', 'none', 'unrestricted', 'suppress'],),
  'z-index': (['auto'],),
}

# Свойства упорядоченные по приоритету (daria)
PRIORITY_PROPERTIES = [
  'display',
  'color',
  'margin',
  'position',
  'padding',
  'width',
  'background',
  'zoom',
  'height',
  'top',
  'vertical-align',
  'overflow',
  'left',
  'margin-right',
  'float',
  'margin-left',
  'cursor',
  'text-decoration',
  'font-size',
  'margin-top',
  'border',
  'background-position',
  'font',
  'margin-bottom',
  'padding-left',
  'right',
  'padding-right',
  'line-height',
  'white-space',
  'text-align',
  'border-color',
  'padding-top',
  'z-index',
  'border-bottom',
  'visibility',
  'border-radius',
  'padding-bottom',
  'font-weight',
  'clear',
  'max-width',
  'border-top',
  'border-width',
  'content',
  'bottom',
  'background-color',
  'opacity',
  'background-image',
  'box-shadow',
  'border-collapse',
  'text-overflow',
  'filter',
  'border-right',
  'text-indent',
  'clip',
  'min-width',
  'min-height',
  'border-left',
  'max-height',
  'border-right-color',
  'border-top-color',
  'transition',
  'resize',
  'overflow-x',
  'list-style',
  'word-wrap',
  'border-left-color',
  'word-spacing',
  'background-repeat',
  'user-select',
  'border-bottom-color',
  'box-sizing',
  'border-top-left-radius',
  'font-family',
  'border-bottom-width',
  'outline',
  'border-bottom-right-radius',
  'border-right-width',
  'border-top-width',
  'font-style',
  'text-transform',
  'border-bottom-left-radius',
  'border-left-width',
  'border-spacing',
  'border-style',
  'border-top-right-radius',
  'text-shadow',
  'border-image',
  'overflow-y',
  'table-layout',
  'background-size',
  'behavior',
  'body',
  'name',
  'letter-spacing',
  'background-clip',
  'pointer-events',
  'transform',
  'counter-reset',
]


# содержит названия всех свойств css (которые смогли найти)
ALL_PROPERTIES = [
  'counter-reset',
  'flex-direction',
  'counter-increment',
  'min-height',
  'quotes',
  'border-top',
  'nav-right',
  'font',
  'white-space-collapse',
  'background-size',
  'list-style-image',
  'background-origin',
  'flex-align',
  'text-emphasis-position',
  'font-stretch',
  'outline-width',
  'border-length',
  'border-right',
  'columns',
  'border-radius',
  'border-bottom-image',
  'box-shadow',
  'border-corner-image',
  'column-rule',
  'border-top-right-radius',
  'word-wrap',
  'text-emphasis-color',
  'border-bottom',
  'border-spacing',
  'max-zoom',
  'column-rule-width',
  'background',
  'list-style-type',
  'nav-left',
  'text-align',
  'border-image-slice',
  'name',
  'overflow-style',
  'page-break-inside',
  'orphans',
  'page-break-before',
  'zoom',
  'break-after',
  'column-span',
  'border-fit',
  'column-fill',
  'tab-size',
  'border-bottom-color',
  'border-bottom-right-radius',
  'line-height',
  'padding-left',
  'text-align-last',
  'font-size',
  'right',
  'transform',
  'outline-color',
  'break-inside',
  'border-top-right-image',
  'text-outline',
  'word-spacing',
  'list-style-position',
  'padding-top',
  'border-image-repeat',
  'border-top-width',
  'bottom',
  'content',
  'border-right-style',
  'padding-right',
  'border-left-style',
  'background-color',
  'column-gap',
  'body',
  'border-left-image',
  'text-emphasis',
  'border-right-image',
  'background-break',
  'animation-delay',
  'unicode-bidi',
  'text-shadow',
  'border-image',
  'max-width',
  'font-family',
  'caption-side',
  'animation-duration',
  'font-emphasize',
  'font-smooth',
  'text-transform',
  'transition',
  'filter',
  'pointer-events',
  'border-right-width',
  'border-image-width',
  'column-rule-color',
  'border-top-style',
  'text-replace',
  'opacity',
  'text-justify',
  'color',
  'border-collapse',
  'border-bottom-width',
  'float',
  'text-height',
  'height',
  'max-height',
  'outline-offset',
  'margin-right',
  'outline-style',
  'background-clip',
  'border-bottom-left-radius',
  'text-emphasis-style',
  'top',
  'border-width',
  'min-width',
  'width',
  'font-variant',
  'border-break',
  'border-top-color',
  'background-position',
  'flex-pack',
  'empty-cells',
  'direction',
  'border-left',
  'animation-play-state',
  'visibility',
  'transition-delay',
  'padding',
  'z-index',
  'background-position-y',
  'text-overflow-mode',
  'background-attachment',
  'overflow',
  'user-select',
  'resize',
  'outline',
  'font-emphasize-style',
  'column-count',
  'user-zoom',
  'font-size-adjust',
  'font-emphasize-position',
  'cursor',
  'column-rule-style',
  'behavior',
  'animation-direction',
  'margin',
  'display',
  'border-left-width',
  'letter-spacing',
  'border-top-left-radius',
  'vertical-align',
  'orientation',
  'clip',
  'border-color',
  'column-width',
  'list-style',
  'margin-left',
  'transform-origin',
  'nav-down',
  'padding-bottom',
  'animation-name',
  'border-bottom-right-image',
  'widows',
  'border',
  'font-style',
  'text-overflow-ellipsis',
  'border-left-color',
  'border-bottom-left-image',
  'break-before',
  'overflow-y',
  'overflow-x',
  'word-break',
  'background-repeat',
  'table-layout',
  'text-overflow',
  'margin-bottom',
  'font-effect',
  'nav-up',
  'animation',
  'border-top-left-image',
  'border-image-outset',
  'font-weight',
  'text-wrap',
  'box-decoration-break',
  'border-right-color',
  'min-zoom',
  'page-break-after',
  'transition-property',
  'text-decoration',
  'white-space',
  'text-indent',
  'nav-index',
  'background-image',
  'flex-order',
  'border-bottom-style',
  'clear',
  'animation-timing-function',
  'border-top-image',
  'border-style',
  'background-position-x',
  'border-image-source',
  'box-sizing',
  'transition-duration',
  'margin-top',
  'animation-iteration-count',
  'hyphens',
  'position',
  'transition-timing-function',
  'left',
]
