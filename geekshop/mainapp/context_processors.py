from mainapp.models import ProductCategories


def basket(request):
    basket_list = []
    if request.user.is_authenticated:
        basket_list = request.user.basket.select_related('product')
    return {
        'basket': basket_list
    }


def categories(request):
    return {'categories': ProductCategories.objects.exclude(is_active=False)}
