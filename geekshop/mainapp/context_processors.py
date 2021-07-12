from basketapp.models import Basket
from mainapp.models import ProductCategories


def basket(request):
    basket_list = []
    if request.user.is_authenticated:
        basket_list = Basket.objects.filter(user=request.user).order_by('product__category')
    return {
        'basket': basket_list
    }


def categories(request):
    return {'categories': ProductCategories.objects.exclude(is_active=False)}
