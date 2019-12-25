import uuid
#from django.conf import settings
#from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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


#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    is_ttv = models.BooleanField(
#        "medicatie verantwoordelijke",
#        default=False,
#        help_text='Bepaalt of de gebruiker medicijnverantwoordelijk is.'
#    )


#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
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

    def __str__(self):
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
        # abstract = True
        verbose_name = 'Medicatie'
        verbose_name_plural = 'Medicatie'


class Drugroute(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    #history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        # abstract = True
        verbose_name = 'Toediening'
        verbose_name_plural = 'Toediening'


class Drugfreq(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    #history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        # abstract = True
        verbose_name = 'Frequentie'
        verbose_name_plural = 'Frequentie'


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


class Prescription(models.Model):
    """"""

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
    m_d00100_p00100 = models.IntegerField(
        verbose_name="m_d00100_p00100", default=0, blank=False, null=False)
    m_d00100_p00200 = models.IntegerField(
        verbose_name="m_d00100_p00200", default=0, blank=False, null=False)
    m_d00100_p00300 = models.IntegerField(
        verbose_name="m_d00100_p00300", default=0, blank=False, null=False)
    m_d00100_p00400 = models.IntegerField(
        verbose_name="m_d00100_p00400", default=0, blank=False, null=False)
    m_d00100_p00500 = models.IntegerField(
        verbose_name="m_d00100_p00500", default=0, blank=False, null=False)

    m_d00200_p00100 = models.IntegerField(
        verbose_name="m_d00200_p00100", default=0, blank=False, null=False)
    m_d00200_p00200 = models.IntegerField(
        verbose_name="m_d00200_p00200", default=0, blank=False, null=False)
    m_d00200_p00300 = models.IntegerField(
        verbose_name="m_d00200_p00300", default=0, blank=False, null=False)
    m_d00200_p00400 = models.IntegerField(
        verbose_name="m_d00200_p00400", default=0, blank=False, null=False)
    m_d00200_p00500 = models.IntegerField(
        verbose_name="m_d00200_p00500", default=0, blank=False, null=False)

    m_d00300_p00100 = models.IntegerField(
        verbose_name="m_d00300_p00100", default=0, blank=False, null=False)
    m_d00300_p00200 = models.IntegerField(
        verbose_name="m_d00300_p00200", default=0, blank=False, null=False)
    m_d00300_p00300 = models.IntegerField(
        verbose_name="m_d00300_p00300", default=0, blank=False, null=False)
    m_d00300_p00400 = models.IntegerField(
        verbose_name="m_d00300_p00400", default=0, blank=False, null=False)
    m_d00300_p00500 = models.IntegerField(
        verbose_name="m_d00300_p00500", default=0, blank=False, null=False)

    m_d00400_p00100 = models.IntegerField(
        verbose_name="m_d00400_p00100", default=0, blank=False, null=False)
    m_d00400_p00200 = models.IntegerField(
        verbose_name="m_d00400_p00200", default=0, blank=False, null=False)
    m_d00400_p00300 = models.IntegerField(
        verbose_name="m_d00400_p00300", default=0, blank=False, null=False)
    m_d00400_p00400 = models.IntegerField(
        verbose_name="m_d00400_p00400", default=0, blank=False, null=False)
    m_d00400_p00500 = models.IntegerField(
        verbose_name="m_d00400_p00500", default=0, blank=False, null=False)

    m_d00500_p00100 = models.IntegerField(
        verbose_name="m_d00500_p00100", default=0, blank=False, null=False)
    m_d00500_p00200 = models.IntegerField(
        verbose_name="m_d00500_p00200", default=0, blank=False, null=False)
    m_d00500_p00300 = models.IntegerField(
        verbose_name="m_d00500_p00300", default=0, blank=False, null=False)
    m_d00500_p00400 = models.IntegerField(
        verbose_name="m_d00500_p00400", default=0, blank=False, null=False)
    m_d00500_p00500 = models.IntegerField(
        verbose_name="m_d00500_p00500", default=0, blank=False, null=False)

    m_d00600_p00100 = models.IntegerField(
        verbose_name="m_d00600_p00100", default=0, blank=False, null=False)
    m_d00600_p00200 = models.IntegerField(
        verbose_name="m_d00600_p00200", default=0, blank=False, null=False)
    m_d00600_p00300 = models.IntegerField(
        verbose_name="m_d00600_p00300", default=0, blank=False, null=False)
    m_d00600_p00400 = models.IntegerField(
        verbose_name="m_d00600_p00400", default=0, blank=False, null=False)
    m_d00600_p00500 = models.IntegerField(
        verbose_name="m_d00600_p00500", default=0, blank=False, null=False)

    m_d00700_p00100 = models.IntegerField(
        verbose_name="m_d00700_p00100", default=0, blank=False, null=False)
    m_d00700_p00200 = models.IntegerField(
        verbose_name="m_d00700_p00200", default=0, blank=False, null=False)
    m_d00700_p00300 = models.IntegerField(
        verbose_name="m_d00700_p00300", default=0, blank=False, null=False)
    m_d00700_p00400 = models.IntegerField(
        verbose_name="m_d00700_p00400", default=0, blank=False, null=False)
    m_d00700_p00500 = models.IntegerField(
        verbose_name="m_d00700_p00500", default=0, blank=False, null=False)

    matrix = models.BooleanField("is matrix filled out", default=False)
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

    def __str__(self):
        return self.name

    def is_lastmod(self):
        return self.lastmod

    def set_lastmod(self, who):

        # when a modification is made, doublecheck flag has to be
        # set back to false
        if self.is_doublecheck():
            self.doublecheck = False

        self.lastmod_who = who
        self.lastmod_when = timezone.now()
        self.lastmod = True
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

    def set_doublecheck(self, who):

        # do not allow the lastmod user to be same as
        # doublecheck user
        if self.lastmod_who == who:
            raise ValidationError(_('lastmod user cannot be the same as doublecheck user.'))
        self.doublecheck_who = who
        self.doublecheck_when = timezone.now()
        self.doublecheck = True
        return self.doublecheck

    def is_matrix(self):
        return self.matrix

    class Meta:
        # abstract = True
        verbose_name = 'Prescriptie'
        verbose_name_plural = 'Prescripties'
