from django import forms
#from django.contrib import admin
#from django_jsonforms.forms import JSONSchemaField
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Div, Field, Submit
from crispy_forms.layout import Submit
from .models import Prescription, Client, Drug

class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'clientForm'
        self.helper.form_class = 'cuneiformForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Opslaan'))

    class Meta:
        model = Client
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'class':'datepicker'}),
                }
        fields = (
            'firstname',
            'lastname',
            'dateofbirth',
            'bsn',
                )
        labels = {
            'firstname': 'Voornaam',
            'lastname': 'Achternaam',
            'dateofbirth': 'Geboortedatum',
            'bsn': 'BSN',
                }
        help_texts = {
            'firstname': 'Voornaam van de client',
            'lastname': 'Achternaam van de client',
            'dateofbirth': 'Geboortedatum van de client in format DD-MM-YYYY',
            'bsn': 'Het 9-cijferig Burger Service Nummer van de client',
            }

class DrugForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DrugForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'drugForm'
        self.helper.form_class = 'cuneiformForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Opslaan'))

    class Meta:
        model = Drug
        fields = (
            'name',
            'ingredient',
            'use',
            'sideeffects',
            'particularities',
            'appearance',
            'intake',
        )
        labels = {
            'name': 'Medicijnnaam',
            'ingredient': 'Werkzame stof',
            'use': 'Voorgeschreven bij',
            'sideeffects': 'Bijwerkingen',
            'particularities': 'Bijzonderheden',
            'appearance': 'Uiterlijk',
            'intake': 'Inname',
        }

class PrescriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'prescriptionForm'
        self.helper.form_class = 'cuneiformForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Opslaan'))

    class Meta:
        model = Prescription
        fields = (
            'name',
            'client',
            'drug',
            'doctor',
            'start_date',
            'end_date',
            'remarks',
        )
        labels = {
            'name': 'Beschrijvende naam',
            'client': 'Client',
            'drug': 'Medicijn',
            'doctor': 'Huisarts',
            'start_date': 'Start datum',
            'end_date': 'Eind datum',
            'remarks': 'Opmerkingen',
        }
        help_texts = {
            'name': 'Beschrijvende naam voor de prescriptie',
            'client': 'De client voor wie de prescriptie voorgeschreven is',
            'drug': 'Het medicijn',
            'doctor': 'De voorschrijvende huisarts',
            'start_date': 'De start datum',
            'end_date': 'De eind datum',
            'remarks': 'Eventuele extra opmerkingen (optioneel)',
        }

class PrescriptionMatrixForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        matrixodict = kwargs.pop('matrixodict')
        super(PrescriptionMatrixForm, self).__init__(*args, **kwargs)
        for daykey, dayvalue in matrixodict.items():
            for key, value in dayvalue.items():
                keyslug = daykey + "_" + key
                self.fields[keyslug] = forms.DecimalField(widget=forms.NumberInput(attrs={'minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number',}))

        self.helper = FormHelper()
        self.helper.form_id = 'PrescriptionMatrixForm'
        self.helper.form_class = 'cuneiform_prescription_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Opslaan'))

    class Meta:
        model = Prescription
        fields = ()
