from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import FormView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse


from .models import Cart, CartItem
from .forms import CartItemAddForm


class CartDetailView(DetailView):
    model = Cart
    template_name = 'carts/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.user:
            raise PermissionDenied
        return obj


class CartItemAddView(FormView):
    form_class = CartItemAddForm
    http_method_names = [u'post',]

    def form_valid(self, form):
        cart = Cart.objects.get(id=self.kwargs.get('pk'))
        if self.request.user != cart.user:
            raise PermissionDenied
        item, created = CartItem.objects.get_or_create(cart=cart, tea=form.cleaned_data['tea'])
        if created:
            messages.add_message(self.request, messages.SUCCESS, "{} was added to your cart.".format(item.tea))
        else:
            messages.add_message(self.request, messages.SUCCESS, "{} was updated in your cart.".format(item.tea))
            item.quantity += 1
            item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('teas:list')


class CartItemDeleteView(DeleteView):
    model = CartItem
    http_method_names = [u'post',]

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        if self.request.user != item.cart.user:
            raise PermissionDenied
        messages.add_message(self.request, messages.SUCCESS, "{} was deleted from your cart.".format(item.tea))
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('carts:detail', kwargs={'pk': self.kwargs.get('cart_pk')})
