from datetime import datetime
import urllib
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from signoff.models import PrescriptionEvent
from .filters import PeFilter


# Create your views here.
def index(request):
    """ index """
    return render(request, 'report_index.html')

@login_required
def ReportOverviewTodayNotsignedoff(request):
    """ View for overview not signed off today """

    dtime_date_today = datetime.today()
    dtime_date_today_str = datetime.today().strftime("%d %B %Y")
    aware_dtime_date_today = make_aware(dtime_date_today)

    # get all prescription events
    #   - only today
    #   - exclude already signedoff
    #   - order by period
    plist = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).order_by('tobe_administered_period')
    
    context = {
        'plist': plist,
        'dtime_date_today': dtime_date_today_str,
    }
    return render(request, 'report_overview_today_notsignedoff.html', context)


@login_required
def ReportOverviewPe(request):
    plist = PrescriptionEvent.objects.all()
    pe_filter = PeFilter(request.GET, queryset=plist)
    return render(request, 'report_overview_pe.html', {'filter': pe_filter})