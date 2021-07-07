from django.db import models
from geekshop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    def position_price(self):
        return self.product.price * self.quantity

    @property
    def total_price(self):
        _positions = Basket.objects.filter(user=self.user)
        _total_price = sum(list(map(lambda x: x.position_price, _positions)))
        return _total_price

    @property
    def total_amount(self):
        _positions = Basket.objects.filter(user=self.user)
        _total_amount = sum(list(map(lambda x: x.quantity, _positions)))
        return _total_amount
