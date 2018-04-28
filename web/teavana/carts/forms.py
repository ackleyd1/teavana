from django import forms
from django.apps import apps

CartItem = apps.get_model('carts', 'CartItem')

class CartItemAddForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['tea',]
