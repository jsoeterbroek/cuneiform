# populate
import os
import sys
import time
import random
import string
from django.utils import timezone
from django.conf import settings
from medslist.models import Client, Prescription, Drug, Doctor
from django.contrib.auth.models import User

start = time.time()
now = timezone.now()
nowstr = now.strftime('%d-%m-%Y %T')

VERBOSE = False
VERBOSE2 = False
DEBUG = False


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class PopUser:

    @classmethod
    def pop_user(cls):
        uname = randomString()
        cls.u = User.objects.create_user(
            username=uname, password='top_secret')
        return cls.u

    def pop_users(self, amount):

        count = 0
        while True:
            if count < amount:
                count += 1
                self.pop_user()
            else:
                break



def run():

    counter_pobjects_all = 0

    populate_user = PopUser()
    populate_user.pop_users(10)

    if VERBOSE:
        print("INFO: start run %s" % nowstr)

    print(" ")
    print("---------------------------------------------")
    print("run stats:")
    print("all prescription objects: %i" % counter_pobjects_all)
    print('It took {0:0.1f} seconds'.format(time.time() - start))
    print("---------------------------------------------")
    print(" ")
