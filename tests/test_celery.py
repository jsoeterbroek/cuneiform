from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
from medslist.models import Drug, Doctor, Client, Prescription
from signoff.tasks import create_pe, update_pe
from signoff.models import PrescriptionEvent


class CeleryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #print("setUpCeleryTestData: Run once to set up non-modified data for all class methods.")
        cls.u1 = User.objects.create_user(username='user1', password='top_secret')
        cls.d1 = Drug.objects.create(
            name='paracetamol', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen'
        )
        cls.doc1 = Doctor.objects.create(firstname='firstname', lastname='lastname')
        cls.c1 = Client.objects.create(
            firstname='firstname', lastname='testclient',
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

    def setUp(self):
        pass

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory',)
    def test_create_pe_noerror(self):
        print("test_create_pe_noerror")
        """Test that the ``create_pe`` task runs with no errors,
        and returns the correct result."""
        p_id = self.p1.pk
        self.assertTrue(create_pe.delay(p_id))

    #def test_update_pe_noerror(self):
    #    print("test_update_pe_noerror")
    #    """Test that the ``update_pe`` task runs with no errors,
    #    and returns the correct result."""
    #    result = update_pe.delay(8)

    #    #self.assertEquals(result.get(), 16)
    #    self.assertTrue(result.successful())
