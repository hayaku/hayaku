# -*- coding: utf-8 -*-
import os

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)

try:
    imp = import_dir('hayaku_dict_driver', ('parse_dict_json',))
    get_css_dict, merge_dict, merge_aliases = imp.get_css_dict, imp.merge_dict, imp.merge_aliases
except ImportError:
    from hayaku_dict_driver import get_css_dict, merge_dict, merge_aliases

hayaku_extra_dicts_cache = {}
hayaku_extra_aliases_cache = {}
hayaku_dict_cache = {}
hayaku_aliases_cache = {}

def get_merged_dict(options):
    global hayaku_extra_dicts_cache
    global hayaku_extra_aliases_cache
    global hayaku_dict_cache
    global hayaku_aliases_cache
    settings = options.get('settings')
    cache_key = 'CSS'
    preprocessor = options.get('CSS_preprocessor')
    if preprocessor:
        cache_key = preprocessor
    result_dict, result_aliases = get_css_dict(preprocessor=preprocessor)

    new_dict = {}
    new_aliases = {}
    extra_scopes = ['user', 'syntax', 'project'] + settings.get('hayaku_extra_scopes', [])

    for scope in extra_scopes:
        dict_name = 'hayaku_' + scope + '_dict'
        alias_name = 'hayaku_' + scope + '_aliases'
        new_dict[dict_name] = settings.get(dict_name, {})
        new_aliases[alias_name] = settings.get(alias_name, {})

        # TODO: use a function for those two if-else noodles
        if 'CSS' in new_dict[dict_name]:
            if preprocessor in new_dict[dict_name]:
                new_dict[dict_name] = merge_dict(new_dict[dict_name].get('CSS'), new_dict[dict_name].get(preprocessor))
            else:
                new_dict[dict_name] = new_dict[dict_name].get('CSS')
        elif preprocessor in new_dict[dict_name]:
            new_dict[dict_name] = new_dict[dict_name].get(preprocessor)

        if 'CSS' in new_aliases[alias_name]:
            if preprocessor in new_aliases[alias_name]:
                new_aliases[alias_name] = merge_dict(new_aliases[alias_name].get('CSS'), new_aliases[alias_name].get(preprocessor))
            else:
                new_aliases[alias_name] = new_aliases[alias_name].get('CSS')
        elif preprocessor in new_aliases[alias_name]:
            new_aliases[alias_name] = new_aliases[alias_name].get(preprocessor)

    if new_dict != hayaku_extra_dicts_cache.get(cache_key):
        hayaku_extra_dicts_cache[cache_key] = new_dict

        for dict_scope in dict(hayaku_extra_dicts_cache.get(cache_key)):
            result_dict = merge_dict(result_dict, hayaku_extra_dicts_cache.get(cache_key).get(dict_scope))

        hayaku_dict_cache[cache_key] = result_dict
    elif cache_key in hayaku_dict_cache:
        result_dict = hayaku_dict_cache[cache_key]

    if new_aliases != hayaku_extra_aliases_cache.get(cache_key):
        hayaku_extra_aliases_cache[cache_key] = new_aliases

        for aliases_scope in dict(hayaku_extra_aliases_cache.get(cache_key)):
            result_aliases = merge_aliases(result_aliases, hayaku_extra_aliases_cache.get(cache_key).get(aliases_scope))

        hayaku_aliases_cache[cache_key] = result_aliases

    elif cache_key in hayaku_aliases_cache:
        result_aliases = hayaku_aliases_cache[cache_key]

    return result_dict, result_aliases
