from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('carts/', include('carts.urls', namespace='carts')),
    path('', include('teas.urls', namespace='teas')),
]
