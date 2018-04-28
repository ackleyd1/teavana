from django.contrib import admin
from django.urls import path, include

from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('carts/', include('carts.urls', namespace='carts')),
    path('teas/', include('teas.urls', namespace='teas')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', HomeView.as_view(), name='home')
]
