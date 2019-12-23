import os
import sys
import pandas as pd
# from datetime import datetime, date, time
import time
from django.utils import timezone
from django.utils.timezone import make_aware
from django.conf import settings
from signoff.models import Signoff, PrescriptionEvent
from signoff.utils import get_period, get_today, get_matrix_lookupkey, calculate_period, is_prescription_signedoff_today_period
from medslist.utils import log_signoff
from log.models import CuneiformLogEntry, SIGNOFF
from medslist.models import Client, Prescription, Drug
from medslist.get_current_user import get_request

start = time.time()
now = timezone.now()
nowstr = now.strftime('%d-%m-%Y %T')

VERBOSE = False
VERBOSE2 = False
DEBUG = False


def run():

    counter_pobjects_all = 0
    counter_pobjects_with_matrixfield_not_zero = 0
    counter_peobjects_all = 0
    counter_peobjects_created = 0
    counter_peobjects_updated = 0
    counter_peobjects_skipped = 0

    if VERBOSE:
        print("INFO: start run %s" % nowstr)

    # get all prescription objects to loop through
    pqs = Prescription.objects.all()
    pqs_count = Prescription.objects.all().count()

    periods = ['p00100', 'p00200', 'p00300', 'p00400', 'p00500']

    if pqs:
        if VERBOSE:
            print("INFO: found %i prescription objects" % pqs_count)

        # main loop through all prescriptions
        for prescription in pqs:
            counter_pobjects_all += 1
            prescription_id = prescription.pk
            prescription_name = prescription.name
            prescription_start_date = prescription.start_date
            prescription_end_date = prescription.end_date
            prescription_drug_id = prescription.drug.pk
            prescription_client_id = prescription.client.pk

            p = Prescription.objects.get(pk=1)

            # prescription_matrix_howmuch = "1"

            if VERBOSE:
                print("INFO: name: %s" % prescription_name)
                print("INFO: start_date: %s" % prescription_start_date)
                print("INFO: end_date: %s" % prescription_end_date)

            # we need to create a prescription event for each day between start_date and end_date
            date_range = pd.date_range(start=prescription_start_date,
                                       end=prescription_end_date).to_pydatetime().tolist()

            for d in date_range:

                for period in periods:
                    counter_peobjects_all += 1
                    # Get the value of the matrix_field
                    # eg. matrix_field = 'm_d00300_p00200'
                    # in order to lookup the right amount of medicine
                    # for a given period on a give weekday based on
                    # a date.
                    weekday_int = d.isoweekday()
                    matrix_field = "m_d00" + \
                        str(weekday_int) + "00_" + period
                    prescription_matrix_howmuch = getattr(
                        prescription, matrix_field)

                    aware_d = make_aware(d)
                    strd = aware_d.strftime('%d, %m, %Y')
                    prescriptionevent_name = str(prescription_id) + "_" + str(prescription_client_id) + \
                        "_" + str(prescription_drug_id) + "_" + period + \
                        "_" + aware_d.strftime('%d%m%Y')

                    # skip all PrescriptionEvents for where the amount of medicine is 1 or more
                    if prescription_matrix_howmuch != 0:
                        counter_pobjects_with_matrixfield_not_zero += 1
                        if VERBOSE:
                            print("INFO: to create or update prescription event with name %s" %
                                  prescriptionevent_name)

                        obj, created = PrescriptionEvent.objects.update_or_create(
                            name=prescriptionevent_name,
                            tobe_administered_date=aware_d,
                            tobe_administered_period=period,
                            tobe_administered_howmuch=prescription_matrix_howmuch,
                            prescription_id=prescription_id,
                            tobe_administered_what_id=prescription_drug_id,
                            tobe_administered_who_id=prescription_client_id
                        )

                        if created:
                            counter_peobjects_created += 1
                            if VERBOSE2:
                                print('INFO: The object was created')
                        else:
                            counter_peobjects_updated += 1
                            if VERBOSE2:
                                print('INFO: The object was updated')
                    else:
                        counter_peobjects_skipped += 1
                        if VERBOSE2:
                            print("INFO: skipping creation prescription event with name %s because prescription_matrix field is zero" %
                                  prescriptionevent_name)

    else:
        if VERBOSE:
            print("INFO: no prescription objects found")

    print(" ")
    print("---------------------------------------------")
    print("run stats:")
    print("all prescription objects: %i" % counter_pobjects_all)
    print("all prescription objects with matrixfield not zero: %i" %
          counter_pobjects_with_matrixfield_not_zero)
    print("all prescription event objects: %i" % counter_peobjects_all)
    print("all prescription event objects created: %i" %
          counter_peobjects_created)
    print("all prescription event objects updated: %i" %
          counter_peobjects_updated)
    print("all prescription event objects skipped: %i" %
          counter_peobjects_skipped)
    print('It took {0:0.1f} seconds'.format(time.time() - start))
    print("---------------------------------------------")
    print(" ")
