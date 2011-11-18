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
