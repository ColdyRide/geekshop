import json
import os

JSON_PATH = 'geekshop/json'


def get_json(file_name):
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='UTF-8') as file:
        result = json.load(file)
    return result


def main_links(request):
    return {'main_links': get_json('main_links')}
