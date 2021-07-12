from django.db import models
from geekshop import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)
    objects = BasketQuerySet.as_manager()

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

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()
