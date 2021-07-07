from django.core.management.base import BaseCommand
from mainapp.models import ProductCategories, Product
from authapp.models import ShopUser

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, f'{file_name}.json'), 'r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategories.objects.all().delete()
        for category in categories:
            new_category = ProductCategories(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_get_param = product["category"]

            if isinstance(category_get_param, int):
                _category = ProductCategories.objects.get(id=category_get_param)
            else:
                _category = ProductCategories.objects.get(name=category_get_param)

            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        super_user = ShopUser.objects.create_superuser('admin', None, '123456', age=30)
