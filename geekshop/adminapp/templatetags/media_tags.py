from django import template

register = template.Library()

URL_PREFIX = '/media/'


@register.filter(name='media_products')
def media_folder_products(string):
    if not string:
        string = 'img/default.jpg'

    new_string = "{}{}".format(URL_PREFIX, string)

    return new_string


@register.filter(name='media_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'

    new_string = "{}{}".format(URL_PREFIX, string)

    return new_string
