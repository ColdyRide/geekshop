from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product
from mainapp.context_processors import basket as cont_basket
from geekshop.context_processors import main_links as cont_main_links


@login_required
def basket(request):
    if request.user.is_authenticated:
        title = 'корзина'
        context = {
            'title': title,
        }

        return render(request, 'basketapp/basket.html', context)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:details', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        # Was added for properly work of ajax basket edition (looks like context_processor for basket ignore this)
        context = cont_basket(request)
        # --------
        result = render_to_string('basketapp/includes/inc_basket_list.html', context, request=request)
        return JsonResponse({'result': result})
