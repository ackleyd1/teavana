from django import forms
from django.apps import apps

from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Div

Tea = apps.get_model('core', 'Tea')

class TeaCreateForm(forms.ModelForm):
    class Meta:
        model = Tea
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'tea-add'
        self.helper.layout.append(HTML("""<div class="form-row mt-2"><input type="submit" value="Submit" class="btn btn-outline-primary btn-block"></div>"""))

class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

class CrispySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

class BraintreeSaleForm(forms.Form):
    payment_method_nonce = forms.CharField()
