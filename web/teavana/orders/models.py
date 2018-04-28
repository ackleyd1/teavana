import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from core.models import TimeStampedModel

class Address(TimeStampedModel):
    address_line_1 = models.CharField(max_length=64)
    address_line_2 = models.CharField(max_length=16, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=32)
    zipcode = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class BillingAddress(Address):
    pass

class ShippingAddress(Address):
    pass

class Order(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT, null=True)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.id})

    def total(self):
        total_price = 0
        for item in self.orderitem_set.all():
            total_price += item.price()
        return total_price

class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    tea = models.ForeignKey('teas.Tea', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def price(self):
        return self.quantity * self.tea.price
