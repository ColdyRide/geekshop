from django.db import models
from django.utils.functional import cached_property

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

    @cached_property
    def get_positions(self):
        return self.user.basket.select_related()

    @property
    def position_price(self):
        return self.product.price * self.quantity

    @property
    def get_summary(self):
        _items = self.get_positions
        return {'total_price': sum(list(map(lambda x: x.position_price, _items))),
                'total_amount ': sum(list(map(lambda x: x.quantity, _items)))}

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()
