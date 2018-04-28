from django import forms
from django.apps import apps

from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.helper import FormHelper


class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class CrispySignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
