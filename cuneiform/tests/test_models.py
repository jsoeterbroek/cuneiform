# tests/test_account.py
from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import User
from medslist.models import DrugManager, Drug, Client, Prescription
from audit_log.models.fields import LastUserField
from django.conf import settings
import datetime
from django.utils import timezone


class DrugModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        Drug.drugs.create(
            name='paracetamol', ingredient='paracetamol', use='headache', sideeffects='more headaches', particularities='geen')

    def test_name_label(self):

        drug = Drug.objects.get(id=1)
        expected_object_name = drug.name
        self.assertEquals(expected_object_name, 'paracetamol')

#        # self.client, _ = Client.create(
#        #        firstname = 'testclient',
#        #        lastname = 'testclient',
#        #        dateofbirth = timezone.now(),
#        #        bsn = '123456789',
#        #        )
#
#    def test_get_prescription(self):
#        print('hallo')
