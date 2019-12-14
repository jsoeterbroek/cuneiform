from django.test import TestCase
from django.test.client import Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from medslist.models import Drug, Prescription, Doctor, Client

class DrugListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        d1 = Drug.objects.create(
            name='paracetamol1', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
        d2 = Drug.objects.create(
            name='paracetamol2', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
        d3 = Drug.objects.create(
            name='paracetamol3', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')

    def setUp(self):
        self.testclient = TestClient()
        self.user = User.objects.create_user('user1', 'lennon@thebeatles.com', 'HoofdPijn')
        self.testclient.login(username='user1', password='HoofdPijn')
           
    def test_view_drug(self):
        print("test_view_drug")
        response = self.testclient.get('/medslist/drug/')
        self.assertEqual(response.status_code, 200)

    def test_view_drug_detail(self):
        print("test_view_drug_detail")
        response = self.testclient.get('/medslist/drug/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_drug_add(self):
        print("test_view_drug_add")
        response = self.testclient.get('/medslist/drug/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_drug_edit(self):
        print("test_view_drug_edit")
        response = self.testclient.get('/medslist/drug/1/edit/')
        self.assertEqual(response.status_code, 200)

class PrescriptionListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        d1 = Drug.objects.create(
            name='paracetamol1', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
        doc1 = Doctor.objects.create(firstname='firstname', lastname='lastname')
        c1 = Client.objects.create(
            firstname='firstname', lastname='testclient',
            dateofbirth='1968-01-22', bsn='122475243'
        )
        c2 = Client.objects.create(
            firstname='firstname', lastname='testclient2',
            dateofbirth='1968-01-22', bsn='122475243'
        )
        Prescription.objects.create_prescription(
            name='prescription test one',
            client=c1,
            drug=d1,
            doctor=doc1,
            remarks='remark',
            start_date='2019-11-10',
            end_date='2019-12-30'
        )

    def setUp(self):
        self.testclient = TestClient()
        self.user = User.objects.create_user('user1', 'lennon@thebeatles.com', 'HoofdPijn')
        self.testclient.login(username='user1', password='HoofdPijn')
           
    def test_view_prescription(self):
        print("test_view_prescription")
        response = self.testclient.get('/medslist/prescription/')
        self.assertEqual(response.status_code, 200)

    def test_view_prescription_detail(self):
        print("test_view_prescription_detail")
        response = self.testclient.get('/medslist/prescription/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_prescription_add(self):
        print("test_view_prescription_add")
        response = self.testclient.get('/medslist/prescription/add/')
        self.assertEqual(response.status_code, 200)

    def test_view_prescription_edit(self):
        print("test_view_prescription_edit")
        response = self.testclient.get('/medslist/prescription/1/edit/')
        self.assertEqual(response.status_code, 200)


