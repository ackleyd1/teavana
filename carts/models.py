import uuid

from django.db import models
from django.conf import settings

from core.models import TimeStampedModel

class CartItem(TimeStampedModel):
    cart = models.ForeignKey('carts.Cart', on_delete=models.CASCADE)
    tea = models.ForeignKey('teas.Tea', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Cart(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField('teas.Tea', through=CartItem)
