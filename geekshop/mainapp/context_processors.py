from mainapp.models import ProductCategories
from django.conf import settings
from django.core.cache import cache

def basket(request):
    basket_list = []
    if request.user.is_authenticated:
        basket_list = request.user.basket.select_related()
    return {
        'basket': basket_list
    }


def categories(request):
    if settings.LOW_CACHE:
        key = 'categories'
        active_categories = cache.get(key)
        if active_categories is None:
            active_categories = ProductCategories.objects.exclude(is_active=False)
            cache.set(key, active_categories)
        return {'categories': active_categories}
    else:
        return {'categories': ProductCategories.objects.exclude(is_active=False)}
