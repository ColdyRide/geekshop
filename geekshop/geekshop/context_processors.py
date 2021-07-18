import json
import os
from django.conf import settings
from django.core.cache import cache

JSON_PATH = 'geekshop/json'


def get_json(file_name):
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='UTF-8') as file:
        result = json.load(file)
    return result


def main_links(request):
    if settings.LOW_CACHE:
        key = 'main_links'
        main_menu = cache.get(key)
        if main_menu is None:
            main_menu = get_json('main_links')
            cache.set(key, main_menu)
        return {'main_links': main_menu}
    else:
        return {'main_links': get_json('main_links')}
