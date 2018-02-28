from django.urls import path

from .views import CartDetailView

app_name='carts'

urlpatterns = [
    path('<uuid:pk>', CartDetailView.as_view(), name='detail'),
]
