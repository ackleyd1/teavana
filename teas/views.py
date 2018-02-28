import braintree

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin

from core.forms import BraintreeSaleForm
from .models import Tea
from .forms import TeaCreateForm

class TeaListView(ListView):
    model = Tea
    template_name = 'teas/tea_list.html'
    context_object_name = 'teas'

class TeaCreateView(CreateView):
    model = Tea
    template_name = 'teas/tea_create.html'
    form_class = TeaCreateForm

    def get_success_url(self):
        return reverse('teas:list')

class TeaDisplayView(DetailView):
    model = Tea
    template_name = 'teas/tea_detail.html'
    context_object_name = 'tea'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['client_token'] = braintree.ClientToken.generate()
        context['sale_form'] = BraintreeSaleForm()
        return context

class TeaSaleView(SingleObjectMixin, FormView):
    model = Tea
    template_name = 'teas/tea_detail.html'
    form_class = BraintreeSaleForm

    def form_valid(self, form):
        nonce = form.cleaned_data['payment_method_nonce']
        tea = self.get_object()
        result = braintree.Transaction.sale({
            "amount": tea.price,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success or result.transaction:
            messages.add_message(self.request, messages.SUCCESS, 'Thank you for buying our tea!')
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse('teas:list')

class TeaDetailView(View):
    def get(self, request, *args, **kwargs):
        view = TeaDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TeaSaleView.as_view()
        return view(request, *args, **kwargs)
