from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """ index """
    return render(request, 'signoff_index.html')

