# tests/test_account.py
#from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import User
from medslist.models import Drug, Doctor, Client, Prescription

class DrugModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        u1 = User.objects.create_user(username='user1', password='top_secret')
        u2 = User.objects.create_user(username='user2', password='top_secret')

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        d1 = Drug.objects.create(
            name='paracetamol', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen'
        )
        doc1 = Doctor.objects.create(firstname='firstname', lastname='lastname')
        c1 = Client.objects.create(
            firstname='firstname', lastname='testclient',
            dateofbirth='1968-01-22', bsn='122475243'
        )
        Prescription.objects.create(
            name='prescription test one',
            client=c1,
            drug=d1,
            doctor=doc1,
            remarks='remark',
            start_date='2019-11-10',
            end_date='2019-12-30'
        )

    def test_name_labels(self):
        print("test_name_label: test name labels")
        drug = Drug.objects.get(id=1)
        self.assertEqual(drug.name, 'paracetamol')
        client = Client.objects.get(id=1)
        self.assertEqual(client.lastname, 'testclient')
        prescription = Prescription.objects.get(id=1)
        self.assertEqual(prescription.name, 'prescription test one')

    def test_get_prescription_lastmod(self):
        u3 = User.objects.create_user(username='user3', password='top_secret')
        p1 = Prescription.objects.get(id=1)
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, False)
        p1.name = "modified prescription test one"
        p1.lastmod_who = u3
        p1.save()
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, True)



