from django import forms
from django.apps import apps

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML

Tea = apps.get_model('teas', 'Tea')

class TeaCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'tea-add'
        self.helper.layout.append(HTML("""<div class="form-row mt-2"><input type="submit" value="Submit" class="btn btn-outline-primary btn-block"></div>"""))

    class Meta:
        model = Tea
        fields = ['name', 'description', 'price', 'image']
