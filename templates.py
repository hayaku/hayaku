# -*- coding: utf-8 -*-

VENDOR_PROPERTY_PREFIXES = {
    'box-shadow': (
        '-webkit-box-shadow',
        '-moz-box-shadow',
        '-o-box-shadow',
        'box-shadow',
    ),
    'box-sizing': (
        '-webkit-box-sizing',
        '-moz-box-sizing',
        'box-sizing',
    ),
    'border-radius': (
        '-webkit-border-radius',
        '-moz-border-radius',
        'border-radius',
    ),
    'user-select': (
        '-webkit-user-select',
        '-moz-user-select',
        'user-select',
    ),
    'transform': (
        '-webkit-transform',
        '-moz-transform',
        '-o-transform',
        'transform',
    ),
    'background-clip': (
        '-webkit-background-clip',
        '-moz-background-clip',
        'background-clip',
    ),
    'border-top-right-radius': (
        '-webkit-border-top-right-radius',
        '-moz-border-radius-topright',
        '-o-border-top-right-radius',
        'border-top-right-radius',
    ),
    'border-top-left-radius': (
        '-webkit-border-top-left-radius',
        '-moz-border-radius-topleft',
        '-o-border-top-left-radius',
        'border-top-left-radius',
    ),
    'border-bottom-right-radius': (
        '-webkit-border-bottom-right-radius',
        '-moz-border-radius-bottomright',
        '-o-border-bottom-right-radius',
        'border-bottom-right-radius',
    ),
    'border-bottom-left-radius': (
        '-webkit-border-bottom-left-radius',
        '-moz-border-radius-bottomleft',
        '-o-border-bottom-left-radius',
        'border-bottom-left-radius',
    ),
}

def align_prefix(prefix):
    prefix_list = VENDOR_PROPERTY_PREFIXES.get(prefix, [])
    if prefix_list:
        # TODO: считать max_length при инициализации VENDOR_PROPERTY_PREFIXES
        max_length = max(len(p) for p in prefix_list)
        # TODO: сделать сортировку по размеру значений в prefix_list
        return tuple((' '*(max_length-len(p))) + p for p in prefix_list)
    return (prefix,)

def make_template(property_, value=None):
    property_ = align_prefix(property_)
    if value is None:
        template_i = ('{0}: ${{1}};${{0}}\n'.format(prop) for prop in property_)
    else:
        template_i = ('{0}: {1};${{0}}'.format(prop, value) for prop in property_)
    return ''.join(template_i)

if __name__ == '__main__':
    print template('box-shadow', 'box')
            
# TODO
# display: -moz-inline-box;
# display: inline-block;

# background-image: -webkit-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:    -moz-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:      -o-linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
# background-image:         linear-gradient(top,rgba(255,255,255,0.6),rgba(255,255,255,0));
