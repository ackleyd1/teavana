from django.contrib import admin
from django.urls import path, include

from .views import TeaListView, TeaCreateView, TeaDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TeaListView.as_view(), name='tea-list'),
    path('create', TeaCreateView.as_view(), name='tea-create'),
    path('<uuid:pk>', TeaDetailView.as_view(), name='tea-detail')
]
