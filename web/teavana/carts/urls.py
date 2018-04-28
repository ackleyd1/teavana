from django.urls import path

from .views import CartDetailView, CartItemAddView, CartItemDeleteView

app_name='carts'

urlpatterns = [
    path('<uuid:pk>', CartDetailView.as_view(), name='detail'),
    path('<uuid:pk>/add', CartItemAddView.as_view(), name='add'),
    path('<uuid:cart_pk>/<int:pk>', CartItemDeleteView.as_view(), name='delete'),
]
