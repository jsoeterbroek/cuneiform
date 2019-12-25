# tests/test_account.py
#from unittest import mock
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#from django.utils import timezone
from medslist.models import Drug, Doctor, Client, Prescription

class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        cls.u1 = User.objects.create_user(username='user1', password='top_secret')
        cls.u2 = User.objects.create_user(username='user2', password='top_secret')
        cls.u3 = User.objects.create_user(username='user3', password='top_secret')
        cls.u4 = User.objects.create_user(username='user4', password='top_secret')
        cls.d1 = Drug.objects.create(
            name='paracetamol', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen'
        )
        cls.doc1 = Doctor.objects.create(firstname='firstname', lastname='lastname')
        cls.c1 = Client.objects.create(
            firstname='firstname', lastname='testclient',
            dateofbirth='1968-01-22', bsn='122475243'
        )
        cls.c2 = Client.objects.create(
            firstname='firstname', lastname='testclient2',
            dateofbirth='1968-01-22', bsn='122475243'
        )
        cls.p1 = Prescription.objects.create(
            name='prescription test one',
            client=cls.c1,
            drug=cls.d1,
            doctor=cls.doc1,
            remarks='remark',
            start_date='2019-11-10',
            end_date='2019-12-30'
        )
        cls.p2 = Prescription.objects.create(
            name='prescription test two',
            client=cls.c2,
            drug=cls.d1,
            doctor=cls.doc1,
            remarks='remark',
            start_date='2019-11-10',
            end_date='2019-12-30'
        )

    def setUp(self):
        #print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_model_client_name_labels(self):
        print("test_model_client_name_label")
        client = Client.objects.get(id=1)
        self.assertEqual(client.lastname, 'testclient')

    def test_model_drug_name_labels(self):
        print("test_model_drug_name_label")
        drug = Drug.objects.get(id=1)
        self.assertEqual(drug.name, 'paracetamol')

    def test_model_prescription_create(self):
        print("test_model_prescription_create")
        Prescription.objects.create(
            name='prescription test two',
            client=self.c2,
            drug=self.d1,
            doctor=self.doc1,
            remarks='remark',
            start_date='2019-11-10',
            end_date='2019-12-30'
        )
        #p3 = Prescription.objects.get(id=3)
        #df = p3.get_pdfmatrix()
        #print(df)

    def test_model_prescription_name_labels(self):
        print("test_model_prescription_name_label")
        prescription = Prescription.objects.get(id=1)
        self.assertEqual(prescription.name, 'prescription test one')

    def test_model_prescription_lastmod(self):
        print("test_model_prescription_lastmod")
        p1 = Prescription.objects.get(id=1)
        u3 = User.objects.get(id=3)
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, False)
        p1.name = "modified prescription test one"
        p1.set_lastmod(u3)
        p1.save()
        is_lastmod = p1.is_lastmod()
        self.assertEqual(is_lastmod, True)

    def test_model_prescription_doublecheck(self):
        """
        scenario:
        user u3 is last one to modify a prescription
          - #1 test that if user to doublecheck is same as last user to modify -> should fail
          - #2 test that if user to doublecheck is different from last user to modify -> should ok
          - #3 test that if prescription is doublechecked, the flag is set back to false, when
               a user has made (newer) modification
        """
        print("test_model_prescription_doublecheck")
        p1 = Prescription.objects.get(id=1)
        p1.name = "modified prescription test one for doublecheck"
        u3 = User.objects.get(id=3)
        u4 = User.objects.get(id=4)
        p1.set_lastmod(u3)
        p1.save()
        # subtest #1
        with self.assertRaises(ValidationError):
            p1.set_doublecheck(u3)
        p1.save()
        # subtest #2
        p1.set_doublecheck(u4)
        p1.save()
        is_doublecheck = p1.is_doublecheck()
        self.assertEqual(is_doublecheck, True)
        # subtest #3
        p1.name = "modified prescription test one for doublecheck again"
        p1.set_lastmod(u3)
        p1.save()
        is_doublecheck = p1.is_doublecheck()
        self.assertEqual(is_doublecheck, False)

    def test_model_prescription_auditlog(self):
        print("test_model_prescription_auditlog")
        