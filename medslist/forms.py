from django import forms
#from django.contrib import admin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
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
        super(PrescriptionMatrixForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.template = 'layout/cuneiform_table_inline_form.html'
        self.helper.layout = Layout(
            Div(
                Field('m_d00100_p00100'),
                Field('m_d00100_p00200'),
                Field('m_d00100_p00300'),
                Field('m_d00100_p00400'),
                Field('m_d00100_p00500'),
                ),
            Div(
                Field('m_d00200_p00100'),
                Field('m_d00200_p00200'),
                Field('m_d00200_p00300'),
                Field('m_d00200_p00400'),
                Field('m_d00200_p00500'),
                ),
            Div(
                Field('m_d00300_p00100'),
                Field('m_d00300_p00200'),
                Field('m_d00300_p00300'),
                Field('m_d00300_p00400'),
                Field('m_d00300_p00500'),
                ),
            Div(
                Field('m_d00400_p00100'),
                Field('m_d00400_p00200'),
                Field('m_d00400_p00300'),
                Field('m_d00400_p00400'),
                Field('m_d00400_p00500'),
                ),
            Div(
                Field('m_d00500_p00100'),
                Field('m_d00500_p00200'),
                Field('m_d00500_p00300'),
                Field('m_d00500_p00400'),
                Field('m_d00500_p00500'),
                ),
            Div(
                Field('m_d00600_p00100'),
                Field('m_d00600_p00200'),
                Field('m_d00600_p00300'),
                Field('m_d00600_p00400'),
                Field('m_d00600_p00500'),
                ),
            Div(
                Field('m_d00700_p00100'),
                Field('m_d00700_p00200'),
                Field('m_d00700_p00300'),
                Field('m_d00700_p00400'),
                Field('m_d00700_p00500'),
                ),
        )
        self.helper.form_id = 'PrescriptionMatrixForm'
        self.helper.form_class = 'hmas_prescription_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Opslaan'))

    class Meta:
        model = Prescription
        fields = (
            'm_d00100_p00100', 'm_d00100_p00200', 'm_d00100_p00300', 'm_d00100_p00400', 'm_d00100_p00500',
            'm_d00200_p00100', 'm_d00200_p00200', 'm_d00200_p00300', 'm_d00200_p00400', 'm_d00200_p00500',
            'm_d00300_p00100', 'm_d00300_p00200', 'm_d00300_p00300', 'm_d00300_p00400', 'm_d00300_p00500',
            'm_d00400_p00100', 'm_d00400_p00200', 'm_d00400_p00300', 'm_d00400_p00400', 'm_d00400_p00500',
            'm_d00500_p00100', 'm_d00500_p00200', 'm_d00500_p00300', 'm_d00500_p00400', 'm_d00500_p00500',
            'm_d00600_p00100', 'm_d00600_p00200', 'm_d00600_p00300', 'm_d00600_p00400', 'm_d00600_p00500',
            'm_d00700_p00100', 'm_d00700_p00200', 'm_d00700_p00300', 'm_d00700_p00400', 'm_d00700_p00500',
            )
        labels = {
            'm_d00100_p00100': 'Maandag',
            'm_d00100_p00200': 'Maandag',
            'm_d00100_p00300': 'Maandag',
            'm_d00100_p00400': 'Maandag',
            'm_d00100_p00500': 'Maandag',
            'm_d00200_p00100': 'Dinsdag',
            'm_d00200_p00200': 'Dinsdag',
            'm_d00200_p00300': 'Dinsdag',
            'm_d00200_p00400': 'Dinsdag',
            'm_d00200_p00500': 'Dinsdag',
            'm_d00300_p00100': 'Woensdag',
            'm_d00300_p00200': 'Woensdag',
            'm_d00300_p00300': 'Woensdag',
            'm_d00300_p00400': 'Woensdag',
            'm_d00300_p00500': 'Woensdag',
            'm_d00400_p00100': 'Donderdag',
            'm_d00400_p00200': 'Donderdag',
            'm_d00400_p00300': 'Donderdag',
            'm_d00400_p00400': 'Donderdag',
            'm_d00400_p00500': 'Donderdag',
            'm_d00500_p00100': 'Vrijdag',
            'm_d00500_p00200': 'Vrijdag',
            'm_d00500_p00300': 'Vrijdag',
            'm_d00500_p00400': 'Vrijdag',
            'm_d00500_p00500': 'Vrijdag',
            'm_d00600_p00100': 'Zaterdag',
            'm_d00600_p00200': 'Zaterdag',
            'm_d00600_p00300': 'Zaterdag',
            'm_d00600_p00400': 'Zaterdag',
            'm_d00600_p00500': 'Zaterdag',
            'm_d00700_p00100': 'Zondag',
            'm_d00700_p00200': 'Zondag',
            'm_d00700_p00300': 'Zondag',
            'm_d00700_p00400': 'Zondag',
            'm_d00700_p00500': 'Zondag',
        }
        help_texts = {
            'm_d00100_p00100': '07:00',
            'm_d00100_p00200': '08:00',
            'm_d00100_p00300': '12:00',
            'm_d00100_p00400': '17:00',
            'm_d00100_p00500': '21:00',
            'm_d00200_p00100': '07:00',
            'm_d00200_p00200': '08:00',
            'm_d00200_p00300': '12:00',
            'm_d00200_p00400': '17:00',
            'm_d00200_p00500': '21:00',
            'm_d00300_p00100': '07:00',
            'm_d00300_p00200': '08:00',
            'm_d00300_p00300': '12:00',
            'm_d00300_p00400': '17:00',
            'm_d00300_p00500': '21:00',
        }
