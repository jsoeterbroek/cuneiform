import uuid
#from django.conf import settings
#from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
#from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from audit_log.models.fields import LastUserField
#from .get_current_user import get_request

#from .utils import log_addition, log_change, log_doublecheck
#from .utils import log_addition

# Logging

ADDITION = 1
CHANGE = 2
DELETION = 3
DOUBLECHECK = 4
SIGNOFF = 5

ACTION_FLAG_CHOICES = (
    (ADDITION, "Toevoegen"),
    (CHANGE, "Aanpassen"),
    (DELETION, "Verwijderen"),
    (DOUBLECHECK, "Dubbelcontrole"),
    (SIGNOFF, "Aftekenen"),
)

CLIENT = 1
DRUG = 2
PRESCRIPTION = 3
SIGNOFF = 4

OBJECT_TYPE_CHOICES = (
    (CLIENT, "Client"),
    (DRUG, "Drug"),
    (PRESCRIPTION, "Prescription"),
    (SIGNOFF, "Signoff"),
)


class CuneiformLogEntryManager(models.Manager):
    use_in_migrations = True

    def log_action(self, username, object_id, object_type, action_flag, change_message=''):
        return self.model.objects.create(
            user=username,
            object_id=str(object_id),
            object_type=object_type,
            action_flag=action_flag,
            change_message=change_message,
        )


class CuneiformLogEntry(models.Model):
    action_time = models.DateTimeField(
        'action time',
        default=timezone.now,
        editable=False,
    )
    user = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.TextField('object id', blank=True, null=True)
    object_type = models.PositiveSmallIntegerField(
        'object type', choices=OBJECT_TYPE_CHOICES)
    action_flag = models.PositiveSmallIntegerField(
        'action flag', choices=ACTION_FLAG_CHOICES)
    change_message = models.TextField('change message', blank=True)

    objects = CuneiformLogEntryManager()

    class Meta:
        verbose_name = 'log entry'
        verbose_name_plural = 'log entries'
        db_table = 'cuneiform_log'
        ordering = ('-action_time',)

    def __repr__(self):
        return str(self.action_time)

    def __str__(self):
        return 'LogEntry Object'

    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION

    def is_doublecheck(self):
        return self.action_flag == DOUBLECHECK

    def is_signoff(self):
        return self.action_flag == SIGNOFF

    def get_edited_object(self):
        """Return the edited object represented by this log entry."""
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    # def last_modified_by(self,object_id,object_type):
    #    return self.
