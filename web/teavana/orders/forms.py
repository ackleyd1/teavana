from django import forms
from django.apps import apps

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML

ShippingAddress = apps.get_model('orders', 'ShippingAddress')
BillingAddress = apps.get_model('orders', 'BillingAddress')

class PaymentForm(forms.Form):
    payment_method_nonce = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(HTML("""<div id="dropin-container"></div><input type="submit" value="Place Order" class="btn btn-outline-primary btn-block" id="submit-button">"""))
        self.helper.form_id = 'payment-form'

    class Meta:
        fields = ['payment_method_nonce']

class BillingAddressCreateForm(forms.ModelForm):
    same_as = forms.BooleanField(required=False, label='Same as shipping address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
        self.helper = FormHelper(self)
        self.helper.layout.append(HTML("""<div class="text-center"><input type="submit" name="submit" value="Submit" class="btn btn-outline-primary"></div>"""))


    class Meta:
        model = BillingAddress
        fields = ['same_as', 'address_line_1', 'address_line_2', 'city', 'state', 'zipcode']
        labels = {
            'address_line_1': 'Address',
            'address_line_2': 'Apt, suite, etc.'
        }

class ShippingAddressCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(HTML("""<div class="text-center"><input type="submit" name="submit" value="Submit" class="btn btn-outline-primary"></div>"""))

    class Meta:
        model = ShippingAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'zipcode']
        labels = {
            'address_line_1': 'Address',
            'address_line_2': 'Apt, suite, etc.'
        }
