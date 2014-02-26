# -*- coding: utf-8 -*-
import os
import sublime

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)

try:
    imp = import_dir('hayaku_dict_driver', ('parse_dict_json',))
    get_css_dict, merge_dict = imp.get_css_dict, imp.merge_dict
except ImportError:
    from hayaku_dict_driver import get_css_dict, merge_dict

hayaku_extra_dicts_cache = {}
hayaku_dict_cache = {}

def get_merged_dict(self, extra_dicts):
    global hayaku_extra_dicts_cache
    global hayaku_dict_cache
    result = get_css_dict()
    new_dict = {}

    def apply_extra_dict(scope):
        dict_name = 'hayaku_' + scope + '_dict'

        got_dict = self.view.settings().get(dict_name)
        if not got_dict:
            return

        new_dict[dict_name] = got_dict

    for got_dict in extra_dicts:
        apply_extra_dict(got_dict)

    if new_dict == hayaku_extra_dicts_cache:
        return hayaku_dict_cache


    hayaku_extra_dicts_cache = new_dict

    for dict_scope in dict(hayaku_extra_dicts_cache):
        result = merge_dict(result, hayaku_extra_dicts_cache.get(dict_scope))

    hayaku_dict_cache = result
    return hayaku_dict_cache
