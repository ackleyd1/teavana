from django.views.generic.detail import DetailView

from .models import Cart

class CartDetailView(DetailView):
    """TODO ensure user"""
    model = Cart
    template_name = 'carts/cart_detail.html'
    context_object_name = 'cart'
