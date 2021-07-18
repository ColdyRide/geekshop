import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import ProductCategories, Product

from django.conf import settings
from django.core.cache import cache


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = \
                Product.objects.all().exclude(category__is_active=False).exclude(is_active=False)\
                    .select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.all().exclude(category__is_active=False).exclude(is_active=False)\
            .select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_in_cat(pk):
    if settings.LOW_CACHE:
        key = f'products_in_cat_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category_id__pk=pk).exclude(category__is_active=False, is_active=False)
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category_id__pk=pk).exclude(category__is_active=False, is_active=False)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategories, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategories, pk=pk)


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    if settings.LOW_CACHE:
        key = f'{hot_product.category}_{hot_product.pk}'
        same_products = cache.get(key)
        if same_products is None:
            same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
            cache.set(key, same_products)
        return same_products
    else:
         return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


class ProductsView(ListView):
    template_name = 'mainapp/products_list.html'
    extra_context = {'title': 'каталог'}
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        if 'pk' in self.kwargs.keys():
            if self.kwargs['pk'] == 1:
                return get_products()
            else:
                return get_products_in_cat(self.kwargs['pk'])
        same_products = get_same_products(self.hot_product)
        return same_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs.keys():
            if self.kwargs['pk'] == 1:
                context['category'] = {'name': 'все'}
            else:
                context['category'] = get_category(self.kwargs['pk'])
            return context
        context['product'] = self.hot_product
        return context

    def get(self, request, *args, **kwargs):
        self.hot_product = get_hot_product()
        self.object_list = self.get_queryset()
        context = self.get_context_data(**kwargs)
        if 'product' in context.keys():
            self.template_name = 'mainapp/products.html'
        return self.render_to_response(context)


def detail(request, pk=None):
    title = 'продукт'
    content = {
        'title': title,
        'product': get_product(pk),
    }

    return render(request, 'mainapp/products.html', content)
