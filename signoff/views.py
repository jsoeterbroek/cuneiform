from datetime import datetime
import urllib
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from log.models import SIGNOFF
from medslist.utils import log_signoff
from medslist.get_current_user import get_request
from .models import PrescriptionEvent
from .utils import get_period, get_today, calculate_period
from .forms import PeForm

@login_required
def index(request):
    """ index """
    return render(request, 'signoff_index.html')

@login_required
def SignoffToday(request):
    """ View for Signoff today """

    dtime_date_today = datetime.today().strftime("%d %B %Y")
    dtime_now = datetime.now()
    period = calculate_period()

    context = {
        'period': period,
        'dtime_date_today': dtime_date_today,
        'dtime_now': dtime_now,
    }
    return render(request, 'signoff_today.html', context)


@login_required
def SignoffTodayPeriod(request, period):
    """ View for Signoff today """

    dtime_date_today = datetime.today()
    dtime_date_today_str = datetime.today().strftime("%d %B %Y")
    aware_dtime_date_today = make_aware(dtime_date_today)
    period_urldecoded = urllib.parse.unquote(period)
    period_hr = get_period()
    weekday_hr = get_today()

    # get all prescription events
    #   - only today
    #   - only this period
    #   - TODO: exclude already signedoff ??
    plist = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).filter(
            tobe_administered_period=period)

    context = {
        'period': period_urldecoded,
        'period_hr': period_hr,
        'plist': plist,
        'dtime_date_today': dtime_date_today_str,
        'weekday_hr': weekday_hr,
    }
    return render(request, 'signoff_today_period.html', context)


@login_required
def SignoffTodayPe(request, pe_id):
    """ View for Signoff today for pe """

    pobj = PrescriptionEvent.objects.get(pk=pe_id)

    if request.method == "POST":
        if pobj:

            form = PeForm()
            pobj.is_signedoff = True
            pobj.is_signedoff_who = get_request().user
            pobj.is_signedoff_when = timezone.now()
            pobj.save()

            user = get_request().user
            obj_type = SIGNOFF
            msg = "Medicatie verstrekking afgetekend"
            log_signoff(user, pobj, obj_type, msg)
            context = {
                'form': form,
                'pobj': pobj,
                'pe_id': pobj.id
            }
            return render(request, 'signoff_today_pe.html', context)

    else:

        form = PeForm()
        context = {
            'pobj': pobj,
            'form': form,
        }
        return render(request, 'signoff_today_pe.html', context)

@login_required
def SignoffTodayPeriodClientSubmit(request):
    """"""

    return render(request, 'signoff_today_period_client_submit.html')


@login_required
def SignoffClient(request):
    """ View for Signoff today """

    return render(request, 'signoff_client.html')

@login_required
def SignoffOverviewTodayNotsignedoff(request):
    """ View for Signoff overview not signed off today """

    dtime_date_today = datetime.today()
    dtime_date_today_str = datetime.today().strftime("%d %B %Y")
    aware_dtime_date_today = make_aware(dtime_date_today)

    # get all prescription events, per period
    #   - only today
    #   - exclude already signedoff
    plist_p00100 = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).filter(tobe_administered_period='p00100')
    plist_p00200 = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).filter(tobe_administered_period='p00200')
    plist_p00300 = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).filter(tobe_administered_period='p00300')
    plist_p00400 = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).filter(tobe_administered_period='p00400')
    plist_p00500 = PrescriptionEvent.objects.all().filter(
        tobe_administered_date=aware_dtime_date_today).exclude(
            is_signedoff=True).filter(tobe_administered_period='p00500')

    context = {
        'plist_p00100': plist_p00100,
        'plist_p00200': plist_p00200,
        'plist_p00300': plist_p00300,
        'plist_p00400': plist_p00400,
        'plist_p00500': plist_p00500,
        'dtime_date_today': dtime_date_today_str,
    }
    return render(request, 'signoff_overview_today_notsignedoff.html', context)
