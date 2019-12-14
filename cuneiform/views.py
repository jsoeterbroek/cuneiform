# views.py
""" Put views here """

from django.http import Http404
#from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def UserProfileView(request, pk):
    """ view """
    user = get_object_or_404(User, pk=pk)
    context = {
        'user': user,
    }
    return render(request, 'registration/profile.html', context)

def MainIndexView(request):
    """ main index view """
    return render(request, 'index.html')

def InfoView(request):
    """ view """
    hmas_versie = settings.CUNEIFORM_VERSION
    context = {
        'versie': hmas_versie,
    }
    return render(request, 'info.html', context)

def LicenseView(request):
    """ license view """
    hmas_versie = settings.CUNEIFORM_VERSION
    context = {
        'versie': hmas_versie,
    }
    return render(request, 'licentie.html', context)

def FeedbackView(request):
    """ view """
    hmas_versie = settings.HMAS_CUNEIFORM_VERSION
    context = {
        'versie': hmas_versie,
    }
    return render(request, 'feedback.html', context)

def VersieView(request):
    """ view """
    hmas_versie = settings.CUNEIFORM_VERSION
    context = {
        'versie': hmas_versie,
    }
    return render(request, 'versie.html', context)
