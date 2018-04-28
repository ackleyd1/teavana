import braintree

from django.db.transaction import TransactionManagementError
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from core.mixins import AdminRequiredMixin
from .models import Order, OrderItem, ShippingAddress, BillingAddress
from .forms import PaymentForm, ShippingAddressCreateForm, BillingAddressCreateForm

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY
    )
)


class OrderListView(AdminRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

class ShippingAddressCreateView(CreateView):
    model = ShippingAddress
    template_name = 'orders/shipping_address_create.html'
    form_class = ShippingAddressCreateForm

    def form_valid(self, form):
        shipping_address = form.save(commit=False)
        shipping_address.user = self.request.user
        shipping_address.save()
        self.request.session.set_expiry(0)
        self.request.session['shipping_id'] = shipping_address.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:billing')

class BillingAddressCreateView(CreateView):
    model = BillingAddress
    template_name = 'orders/billing_address_create.html'
    form_class = BillingAddressCreateForm

    def dispatch(self, request, *args, **kwargs):
        if 'shipping_id' not in request.session:
            raise TransactionManagementError
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        elif form.data['same_as']:
            shipping_address =  ShippingAddress.get(pk=request.session['shipping_id'])
            data = {}
            data['address_line_1'] = shipping_address.address_line_1
            data['address_line_2'] = shipping_address.address_line_2
            data['city'] = shipping_address.city
            data['state'] = shipping_address.state
            data['zipcode'] = shipping_address.zipcode
            form.data = data
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        billing_address = form.save(commit=False)
        billing_address.user = self.request.user
        billing_address.save()
        self.request.session['billing_id'] = billing_address.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:create')


class OrderCreateView(FormView):
    template_name = 'orders/payment.html'
    form_class = PaymentForm

    def dispatch(self, request, *args, **kwargs):
        if 'billing_id' not in request.session or 'shipping_id' not in request.session:
            raise TransactionManagementError
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['client_token'] = gateway.client_token.generate()
        return context

    def get_success_url(self):
        return reverse('orders:detail', kwargs={'pk': self.order.id})

    def form_valid(self, form):
        nonce = form.cleaned_data['payment_method_nonce']
        result = gateway.transaction.sale({
            "amount": self.request.user.cart.total(),
            "payment_method_nonce": nonce,
            "options": {
              "submit_for_settlement": True
            }
        })
        if result.is_success or result.transaction:
            messages.add_message(self.request, messages.SUCCESS, 'Thank you for ordering!')
            order_data = {}
            order_data['shipping_address'] = ShippingAddress.objects.get(pk=self.request.session['shipping_id'])
            order_data['billing_address'] = BillingAddress.objects.get(pk=self.request.session['billing_id'])
            order_data['user'] = self.request.user
            order = Order.objects.create(**order_data)
            for cart_item in self.request.user.cart.cartitem_set.all():
                tea = cart_item.tea
                quantity = cart_item.quantity
                OrderItem.objects.create(order=order, tea=tea, quantity=quantity)
            for cart_item in self.request.user.cart.cartitem_set.all():
                cart_item.delete()
            self.order = order
        return super().form_valid(form)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and self.request.user != obj.user:
            raise PermissionDenied
        return obj
