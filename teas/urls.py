from django.urls import path

from .views import TeaListView, TeaCreateView, TeaDetailView

app_name='teas'

urlpatterns = [
    path('', TeaListView.as_view(), name='list'),
    path('create', TeaCreateView.as_view(), name='create'),
    path('<uuid:pk>', TeaDetailView.as_view(), name='detail')
]
