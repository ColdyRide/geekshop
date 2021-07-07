import random

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import ProductCategories, Product


def get_hot_product():
    products = Product.objects.all().exclude(category__is_active=False)
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


class ProductsView(ListView):
    template_name = 'mainapp/products_list.html'
    extra_context = {'title': 'каталог'}
    paginate_by = 3
    context_object_name = 'products'

    def get_queryset(self):
        if 'pk' in self.kwargs.keys():
            if self.kwargs['pk'] == 1:
                return Product.objects.all().exclude(category__is_active=False).order_by('price')
            else:
                return Product.objects.filter(category_id__pk=self.kwargs['pk']).exclude(
                    category__is_active=False).order_by('price')
        same_products = get_same_products(self.hot_product)
        return same_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'pk' in self.kwargs.keys():
            if self.kwargs['pk'] == 1:
                context['category'] = {'name': 'все'}
            else:
                context['category'] = get_object_or_404(ProductCategories, pk=self.kwargs['pk'])
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
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/products.html', content)
