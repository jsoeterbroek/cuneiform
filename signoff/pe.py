import time
import string
import random
import pandas as pd
from celery.decorators import task
from django.utils import timezone
from django.utils.timezone import make_aware
from signoff.models import PrescriptionEvent
from medslist.models import Prescription

start = time.time()
now = timezone.now()
nowstr = now.strftime('%d-%m-%Y %T')


def random_gen(size=18, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@task(name='create_pe')
def create_pe(prescription_id):

    periods = ['p00100', 'p00200', 'p00300', 'p00400', 'p00500']
    p = Prescription.objects.get(pk=prescription_id)
    prescription_id = p.pk
    prescription_start_date = p.start_date
    prescription_end_date = p.end_date
    prescription_drug_id = p.drug.pk
    prescription_client_id = p.client.pk
    # we need to create a prescription event for each day between start_date and end_date
    date_range = pd.date_range(start=prescription_start_date,
                               end=prescription_end_date).to_pydatetime().tolist()
    for d in date_range:
        for period in periods:
            weekday_int = d.isoweekday()
            matrix_field = "m_d00" + \
                str(weekday_int) + "00_" + period
            pe_matrix_howmuch = getattr(p, matrix_field)
            aware_d = make_aware(d)
            pe_name = random_gen()
            # skip all PrescriptionEvents for where the amount of medicine is 1 or more
            if pe_matrix_howmuch != 0:
                PrescriptionEvent.objects.create(
                    name=pe_name,
                    tobe_administered_date=aware_d,
                    tobe_administered_period=period,
                    tobe_administered_howmuch=pe_matrix_howmuch,
                    prescription_id=prescription_id,
                    tobe_administered_what_id=prescription_drug_id,
                    tobe_administered_who_id=prescription_client_id
                )


@task(name='update_pe')
def update_pe(prescription_id):

    periods = ['p00100', 'p00200', 'p00300', 'p00400', 'p00500']
    p = Prescription.objects.get(pk=prescription_id)
    prescription_id = p.pk
    prescription_start_date = p.start_date
    prescription_end_date = p.end_date
    prescription_drug_id = p.drug.pk
    prescription_client_id = p.client.pk
    # we need to create a prescription event for each day between start_date and end_date
    date_range = pd.date_range(start=prescription_start_date,
                               end=prescription_end_date).to_pydatetime().tolist()

    # simply delete all prescriptionevents belonging to prescription and re-create
    PrescriptionEvent.objects.all().filter(prescription_id=prescription_id).delete()

    for d in date_range:
        for period in periods:
            weekday_int = d.isoweekday()
            matrix_field = "m_d00" + \
                str(weekday_int) + "00_" + period
            pe_matrix_howmuch = getattr(p, matrix_field)
            aware_d = make_aware(d)
            pe_name = random_gen()
            # skip all PrescriptionEvents for where the amount of medicine is 1 or more
            if pe_matrix_howmuch != 0:
                PrescriptionEvent.objects.create(
                    name=pe_name,
                    tobe_administered_date=aware_d,
                    tobe_administered_period=period,
                    tobe_administered_howmuch=pe_matrix_howmuch,
                    prescription_id=prescription_id,
                    tobe_administered_what_id=prescription_drug_id,
                    tobe_administered_who_id=prescription_client_id
                )
