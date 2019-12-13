# tests/test_account.py
#from unittest import mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#from django.utils import timezone
from medslist.models import Drug, Doctor, Client, Prescription

class DrugModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        u1 = User.objects.create_user(username='user1', password='top_secret')
        u2 = User.objects.create_user(username='user2', password='top_secret')
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

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_name_labels(self):
        print("test_name_label: test name labels")
        drug = Drug.objects.get(id=1)
        self.assertEqual(drug.name, 'paracetamol')
        client = Client.objects.get(id=1)
        self.assertEqual(client.lastname, 'testclient')
        prescription = Prescription.objects.get(id=1)
        self.assertEqual(prescription.name, 'prescription test one')

    def test_prescription_lastmod(self):
        print("test_prescription_lastmod: test prescription lastmod")
        u3 = User.objects.create_user(username='user3', password='top_secret')
        p1 = Prescription.objects.get(id=1)
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, False)
        p1.name = "modified prescription test one"
        p1.set_lastmod(u3)
        p1.save()
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, True)

    def test_prescription_lastdoublecheck(self):
        """
        scenario:
        user u3 is last one to modify a prescription
          - #1 test that if user to doublecheck is same as last user to modify -> should fail
          - #2 test that if user to doublecheck is different from last user to modify -> should ok
          - #3 test that if prescription is doublechecked, the flag is set back to false, when
               a user has made (newer) modification
        """
        print("test_prescription_lastdoublecheck: test prescription lastdoublecheck")
        u3 = User.objects.create_user(username='user3', password='top_secret')
        u4 = User.objects.create_user(username='user4', password='top_secret')
        p1 = Prescription.objects.get(id=1)
        p1.name = "modified prescription test one for doublecheck"
        p1.set_lastmod(u3)
        p1.save()
        # #1
        with self.assertRaises(ValidationError):
            p1.set_doublecheck(u3)
        p1.save()
        # #2
        p1.set_doublecheck(u4)
        p1.save()
        is_doublecheck = p1.is_doublecheck()
        self.assertEqual(is_doublecheck, True)
        # #3
        p1.name = "modified prescription test one for doublecheck again"
        p1.set_lastmod(u3)
        p1.save()
        is_doublecheck = p1.is_doublecheck()
        self.assertEqual(is_doublecheck, False)

    def test_prescription_matrix(self):
        print("test_prescription_matrix: test prescription matrix")
        pass

    def test_prescription_auditlog(self):
        print("test_prescription_auditlog: test prescription auditlog")
        pass


