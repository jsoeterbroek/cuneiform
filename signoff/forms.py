from django import forms
#from django.contrib import admin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden, Field, Submit
from .models import PrescriptionEvent

class PeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'peForm'
        self.helper.form_class = 'cuneiformForm'
        self.helper.add_input(Submit('submit', 'Aftekenen'))

    class Meta:
        model = PrescriptionEvent
        fields = []
