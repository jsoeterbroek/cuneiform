import uuid
#from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from audit_log.models.fields import LastUserField
from medslist.models import Prescription, Drug, Client


class PrescriptionEvent(models.Model):
    """ Prescription event model"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(_('Prescrition name'), max_length=255, unique=True,
                            help_text=_('The descriptive name of the prescription event'))
    created = models.DateTimeField(auto_now_add=True, null=True)
    history = HistoricalRecords()
    prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT)
    tobe_administered_date = models.DateField(_('Prescription event date'), null=True, blank=True,
                                              help_text=_('The date of the prescription event'))
    tobe_administered_period = models.CharField(
        _('Prescription event period'), max_length=6)
    tobe_administered_who = models.ForeignKey(Client, on_delete=models.PROTECT)
    tobe_administered_what = models.ForeignKey(Drug, on_delete=models.PROTECT)
    tobe_administered_howmuch = models.IntegerField()
    is_signedoff = models.BooleanField(
        _('Prescription event signed off'), default=False, help_text=_('Prescription event is signed off or not'))
    is_signedoff_who = LastUserField(
        on_delete=models.PROTECT, related_name="is_signedoff_who", editable=True, null=True, blank=True)
    is_signedoff_when = models.DateTimeField(_('Prescription event signed off when'),
                                             null=True, blank=True)

    def __str__(self):
        return self.name

    def is_signoff(self):
        return self.signoff

    def get_signoff_who(self):
        return self.signoff_who

    def get_signoff_when(self):
        return self.signoff_when

    def get_period(self):
        return self.period

    class Meta:
        verbose_name = _('Prescription event')
        verbose_name_plural = _('Prescription events')


class Signoff(models.Model):
    """ Signoff model """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    signoff = models.BooleanField("prescription is signed off", default=False)
    signoff_who = LastUserField(
        on_delete=models.PROTECT, related_name="signoff_who", editable=True)
    signoff_when = models.DateTimeField(
        "signoff_when", null=True, blank=True)
    signoff_weekday = models.IntegerField()
    signoff_period = models.IntegerField()
    prescription = models.ForeignKey(Prescription, on_delete=models.PROTECT)
    period = models.CharField(blank=True, null=True, max_length=15)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Afteken actie'
        verbose_name_plural = 'Afteken acties'
