from django.shortcuts import render

# Create your views here.
def index(request):
    """ index """
    return render(request, 'report_index.html')
