from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse

from .models import Cart, CartItem
from .forms import CartItemAddForm

class CartDetailView(DetailView):
    """TODO ensure user"""
    model = Cart
    template_name = 'carts/cart_detail.html'
    context_object_name = 'cart'

class CartItemAddView(FormView):
    """TODO ensure user"""
    form_class = CartItemAddForm
    http_method_names = [u'post',]

    def form_valid(self, form):
        cart = Cart.objects.get(id=self.kwargs.get('pk'))
        item, created = CartItem.objects.get_or_create(cart=cart, tea=form.cleaned_data['tea'])
        if not created:
            item.quantity += 1
            item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('carts:detail', kwargs={'pk': self.kwargs.get('pk')})

class CartItemDeleteView(DeleteView):
    model = CartItem
    http_method_names = [u'post',]

    def get_success_url(self):
        return reverse('carts:detail', kwargs={'pk': self.kwargs.get('cart_pk')})
