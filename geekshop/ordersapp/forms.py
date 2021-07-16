from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='цена', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = \
            Product.objects.filter(category__is_active=True, is_active=True)\
            .exclude(quantity=0)\
            .order_by('category', 'name').select_related()
        for field_name, field in self.fields.items():
            if field_name == 'product':
                field.widget.attrs['class'] = 'form-select'
                continue
            if field_name == 'quantity' and self.instance.id:
                field.widget.attrs['max'] = self.instance.product.quantity
            field.widget.attrs['class'] = 'form-control'
