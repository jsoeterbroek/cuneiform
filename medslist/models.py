import uuid
#from django.conf import settings
#from datetime import datetime
import pickle
import base64
import numpy as np
import pandas as pd
from django.db import models
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import User
#from django.utils.dateparse import parse_datetime
from django.utils import timezone
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from audit_log.models.fields import LastUserField
#from .get_current_user import get_request

#from .utils import log_addition, log_change, log_doublecheck
#from .utils import log_addition

# class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    is_ttv = models.BooleanField(
#        "medicatie verantwoordelijke",
#        default=False,
#        help_text='Bepaalt of de gebruiker medicijnverantwoordelijk is.'
#    )

#@receiver(post_save, sender=User)
# def create_user_profile(instance, created):
#    if created:
#        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
# def save_user_profile(instance):
#    instance.profile.save()


class Drug(models.Model):
    """ Drug model """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField("naam", max_length=255,
                            help_text="De naam van het medicijn")
    ingredient = models.CharField(max_length=255)
    use = models.CharField("Te gebruiken bij", max_length=255, help_text="")
    sideeffects = models.TextField("Mogelijke bijwerkingen",
                                   help_text="Mogelijke bijwerkingen van dit medicijn")
    particularities = models.CharField(
        "Bijzonderheden", max_length=255, help_text="Bijzonderheden")
    appearance = models.CharField(
        "Uiterlijk", max_length=255, help_text="Uiterlijk")
    intake = models.CharField("Inname", max_length=255,
                              help_text="Wijze van inname")
    lastmod = models.BooleanField("is last modified", default=False)
    lastmod_who = LastUserField(
        on_delete=models.PROTECT, related_name="drug_lastmod_who")
    lastmod_when = models.DateTimeField(
        "date is last modified", null=True, blank=True)
    doublecheck = models.BooleanField("is doublechecked", default=False)
    doublecheck_who = LastUserField(
        on_delete=models.PROTECT, related_name="drug_doublecheck_who")
    doublecheck_when = models.DateTimeField(
        "date is doublechecked", null=True, blank=True)
    history = HistoricalRecords()
    #drugs = DrugManager()

    def __str__(self):
        return self.name

    def get_lastmod_when(self):
        return self.lastmod_when

    def is_doublecheck(self):
        return self.doublecheck

    def get_doublecheck_who(self):
        return self.doublecheck_who

    def get_doublecheck_when(self):
        return self.doublecheck_when

    def is_lastmod(self):
        return self.lastmod

    def get_lastmod_who(self):
        return self.lastmod_who

    class Meta:
        # abstract = True
        verbose_name = 'Medicatie'
        verbose_name_plural = 'Medicatie'


class Doctor(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    #history = HistoricalRecords()

    def __str__(self):
        self.name = self.firstname + ' ' + self.lastname
        return self.name

    class Meta:
        verbose_name = 'Huisarts'
        verbose_name_plural = 'Huisartsen'


class Client(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dateofbirth = models.DateField()
    bsn = models.CharField(max_length=9)
    created = models.DateTimeField(auto_now_add=True)
    lastmod = models.BooleanField("is last modified", default=False)
    lastmod_who = LastUserField(
        on_delete=models.PROTECT, related_name="client_lastmod_who")
    lastmod_when = models.DateTimeField(
        "date is last modified", null=True, blank=True)
    doublecheck = models.BooleanField("is doublechecked", default=False)
    doublecheck_who = LastUserField(
        on_delete=models.PROTECT, related_name="client_doublecheck_who")
    doublecheck_when = models.DateTimeField(
        "date is doublechecked", null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        self.name = self.firstname + ' ' + self.lastname
        return self.name

    def is_lastmod(self):
        return self.lastmod

    def get_lastmod_who(self):
        return self.lastmod_who

    def get_lastmod_when(self):
        return self.lastmod_when

    def is_doublecheck(self):
        return self.doublecheck

    def get_doublecheck_who(self):
        return self.doublecheck_who

    def get_doublecheck_when(self):
        return self.doublecheck_when

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clienten'

class PrescriptionManager(models.Manager):
    """ Prescription Model Manager """

    def create(self, *args, **kwargs):

        #initial 2-d numpy matrix 42 range, seven days, six periods
        arr = np.arange(42)
        zz = np.zeros(arr.shape)
        npmatrix = zz.reshape(6, 7) # six periods, seven days
        matrix_bytes = pickle.dumps(npmatrix)
        matrix_base64 = base64.b64encode(matrix_bytes)
        matrix = matrix_base64
        kwargs['matrix'] = matrix
        return super(PrescriptionManager, self).create(*args, **kwargs)   

class Prescription(models.Model):
    """ Prescription Model """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=250)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    #route = models.ForeignKey(Drugroute, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    #frequency = models.ForeignKey(Drugfreq, on_delete=models.CASCADE)
    matrix = models.BinaryField()
    matrix_hr_summary = models.TextField(default="", blank=False, null=False)
    lastmod = models.BooleanField("is last modified", default=False)
    lastmod_who = LastUserField(
        on_delete=models.PROTECT, related_name="presciption_lastmod_who")
    lastmod_when = models.DateTimeField(
        "date is last modified", null=True, blank=True)
    doublecheck = models.BooleanField("is doublechecked", default=False)
    doublecheck_who = LastUserField(
        on_delete=models.PROTECT, related_name="presciption_doublecheck_who")
    doublecheck_when = models.DateTimeField(
        "date is doublechecked", null=True, blank=True)
    history = HistoricalRecords()
    objects = PrescriptionManager()

    def __str__(self):
        return self.name

    def update_matrix(self, period, day, value):
        """
        takes 3 arguments:
         - period (one of: 'p00100','p00200','p00300','p00400','p00500','p00600') 
         - day (one of: 'mon','tue','wed','thu','fri','sat','sun')
         - value
        e.g.:
        p1.update_matrix('p00400', 'sat', 12) # value 12 on 4th period on saturday
        """
        valid_periods = {'p00100','p00200','p00300','p00400','p00500','p00600'}
        if period not in valid_periods:
            raise ValueError("results: period must be one of %s." % valid_periods)
        valid_days = {'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'}
        if day not in valid_days:
            raise ValueError("results: day must be one of %s." % valid_days)
        df = self.get_pdfmatrix()
        df.at[period, day] = value
        self.set_pdfmatrix(df)

    def get_npmatrix(self):
        """retrieve matrix from database, return a numpy 2d array"""
        matrix_bytes = base64.b64decode(self.matrix)
        npmatrix = pickle.loads(matrix_bytes)
        return npmatrix

    def get_pdfmatrix(self):
        """argument numpy matrix, return a pandas dataframe"""
        _npmatrix = self.get_npmatrix()
        column_names = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        row_names = ['p00100', 'p00200', 'p00300', 'p00400', 'p00500', 'p00600']
        pdfmatrix = pd.DataFrame(_npmatrix, columns=column_names, index=row_names)
        return pdfmatrix

    def set_npmatrix(self, _npmatrix):
        """set numpy matrix to db"""
        matrix_bytes = pickle.dumps(_npmatrix)
        matrix_base64 = base64.b64encode(matrix_bytes)
        self.matrix = matrix_base64

    def set_pdfmatrix(self, _pdfmatrix):
        """convert pandas dataframe to numpy, then set to db"""
        _npmatrix = _pdfmatrix.to_numpy()
        self.set_npmatrix(_npmatrix)

    def is_lastmod(self):
        return self.lastmod

    def get_lastmod_who(self):
        return self.lastmod_who

    def get_lastmod_when(self):
        return self.lastmod_when

    def set_lastmod(self, who):

        # when a modification is made, doublecheck flag has to be
        # set back to false
        if self.is_doublecheck():
            self.doublecheck = False

        self.lastmod_who = who
        self.lastmod_when = timezone.now()
        self.lastmod = True
        return self.lastmod

    def is_doublecheck(self):
        return self.doublecheck

    def get_doublecheck_who(self):
        return self.doublecheck_who

    def get_doublecheck_when(self):
        return self.doublecheck_when

    def set_doublecheck(self, who):

        # do not allow the lastmod user to be same as
        # doublecheck user
        if self.lastmod_who == who:
            raise ValidationError(_('lastmod user cannot be the same as doublecheck user.'))
        self.doublecheck_who = who
        self.doublecheck_when = timezone.now()
        self.doublecheck = True
        return self.doublecheck

    class Meta:
        # abstract = True
        verbose_name = 'Prescriptie'
        verbose_name_plural = 'Prescripties'
