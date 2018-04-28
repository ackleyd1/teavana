from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.views.generic.list import ListView

from core.mixins import AdminRequiredMixin
from .models import Tea
from .forms import TeaCreateForm


class TeaListView(ListView):
    model = Tea
    template_name = 'teas/tea_list.html'
    context_object_name = 'teas'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        type = self.request.GET.get('type')
        if type:
            qs = qs.filter(type=type)
        return qs


class TeaCreateView(AdminRequiredMixin, CreateView):
    model = Tea
    template_name = 'teas/tea_create.html'
    form_class = TeaCreateForm

    def get_success_url(self):
        return reverse('teas:list')


class TeaDetailView(DetailView):
    model = Tea
    template_name = 'teas/tea_detail.html'
    context_object_name = 'tea'
