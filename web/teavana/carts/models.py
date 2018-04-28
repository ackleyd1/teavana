import uuid

from django.db import models
from django.conf import settings

from core.models import TimeStampedModel


class CartItem(TimeStampedModel):
    cart = models.ForeignKey('carts.Cart', on_delete=models.CASCADE)
    tea = models.ForeignKey('teas.Tea', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def price(self):
        return self.quantity * self.tea.price


class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('teas.Tea', through=CartItem)

    def total(self):
        total_price = 0
        for item in self.cartitem_set.all():
            total_price += item.price()
        return total_price
