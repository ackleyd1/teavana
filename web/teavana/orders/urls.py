from django.urls import path

from .views import OrderListView, ShippingAddressCreateView, BillingAddressCreateView, OrderCreateView, OrderDetailView

app_name='orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='list'),
    path('checkout/shipping', ShippingAddressCreateView.as_view(), name='shipping'),
    path('checkout/billing', BillingAddressCreateView.as_view(), name='billing'),
    path('checkout/payment', OrderCreateView.as_view(), name='create'),
    path('<uuid:pk>', OrderDetailView.as_view(), name='detail')
]
