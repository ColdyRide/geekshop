from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


class FormValidMixin:
    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class AjaxMixinGet:

    def get(self, request, *args, **kwargs):
        if request.resolver_match.url_name == 'order_create':
            self.object = None
        else:
            self.object = super().get_object()
        context = self.get_context_data()
        if self.request.is_ajax():
            product_id = self.request.GET.get('product_id')
            if product_id:
                new_product = Product.objects.filter(pk=int(product_id)).get()
                context['new_product'] = {'price': new_product.price,
                                          'quantity': new_product.quantity}
                return JsonResponse(context['new_product'])
        return self.render_to_response(context)


class OrderList(ListView):
    model = Order
    extra_context = {'title': 'заказы'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(FormValidMixin,AjaxMixinGet, CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')
    extra_context = {'title': 'заказы/создание'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            # basket_items = Basket.objects.filter(user=self.request.user)
            basket_items = self.request.user.basket.select_related()
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        return context


class OrderUpdate(FormValidMixin, AjaxMixinGet, UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:order_list')
    extra_context = {'title': 'заказы/изменение'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:order_list')


class OrderRead(DetailView):
    model = Order
    extra_context = {'title': 'заказы/просмотр'}


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:order_list'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.objects.get(pk=instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()
