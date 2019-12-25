# views.py
""" Put views here """

from django.http import Http404
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.urls import reverse_lazy
#from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.utils import timezone
#from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from log.models import CuneiformLogEntry, DRUG, CLIENT, PRESCRIPTION
from signoff.pe import create_pe, update_pe
from .forms import PrescriptionForm, PrescriptionMatrixForm, ClientForm, DrugForm
from .models import Prescription, Client, Drug
from .utils import log_addition, log_change, log_doublecheck
from .get_current_user import get_request

def index(request):
    """ index """
    return render(request, 'medslist_index.html')

@login_required
def UserProfileView(request):
    """ view """
    context = {}
    return render(request, 'accounts/profile.html', context)

# mag alleen door TTV-ers gezien worden
# if statement in template
@login_required
def LogListView(request):
    """ log list view with pagination """

    log_list_latest = CuneiformLogEntry.objects.order_by('-action_time')[:250]
    paginator = Paginator(log_list_latest, 20)
    page = request.GET.get('page')
    try:
        plist = paginator.get_page(page)
    except PageNotAnInteger:
        plist = paginator.get_page(1)
    except EmptyPage:
        plist = paginator.get_page(paginator.num_pages)

    context = {'plist': plist}
    return render(request, 'log/log_list.html', context)

@login_required
def OverviewDoublecheckListView(request):
    """ not emplty"""
    list_latest = CuneiformLogEntry.objects.order_by('-action_time')[:75]
    context = {
        'list': list_latest,
    }
    return render(request, 'overview_doublecheck_list.html', context)


@login_required
def DrugListView(request):
    """ List view (index) or Drug objects """

    drug_list_latest = Drug.objects.order_by('name')
    paginator = Paginator(drug_list_latest, 15)
    page = request.GET.get('page')
    try:
        plist = paginator.get_page(page)
    except PageNotAnInteger:
        plist = paginator.get_page(1)
    except EmptyPage:
        plist = paginator.get_page(paginator.num_pages)

    context = {'plist': plist}
    return render(request, 'drug_index.html', context)


@login_required
def DrugDoublecheckView(request, pk):
    """ Doublecheck view of Drug object """
    try:
        drug = Drug.objects.get(pk=pk)
    except Drug.DoesNotExist:
        raise Http404("drug does not exist")

    lastmod_who = 'Unknown'
    request_who = ''
    if drug.is_lastmod():
        lastmod_who = drug.get_lastmod_who()
        request_who = get_request().user
    context = {
        'drug': drug,
        'lastmod_who': lastmod_who,
        'request_who': request_who,
    }
    return render(request, 'drug_doublecheck.html', context)


@login_required
def DrugDoublecheckNextView(request, pk):
    """ DoublecheckNext view of Drug object """
    try:
        drug = Drug.objects.get(pk=pk)
    except Drug.DoesNotExist:
        raise Http404("drug does not exist")

    user = get_request().user
    obj_type = DRUG
    msg = "Medicijn %s is dubbelgecontroleerd" % drug.name
    drug.doublecheck = True
    drug.doublecheck_who = get_request().user
    drug.doublecheck_when = timezone.now()
    drug.save()
    log_doublecheck(user, drug, obj_type, msg)
    return redirect('drug-detail', pk=drug.pk)


@login_required
def DrugDetailView(request, pk):
    """ Detail view (index) or Drug object """
    try:
        drug = Drug.objects.get(pk=pk)
    except Drug.DoesNotExist:
        raise Http404("drug does not exist")

    lastmod = drug.is_lastmod()
    lastmod_who = ''
    lastmod_when = ''
    doublecheck = drug.is_doublecheck()
    doublecheck_who = ''
    doublecheck_when = ''
    if drug.is_lastmod():
        lastmod_who = drug.get_lastmod_who()
        lastmod_when = drug.get_lastmod_when()
    if drug.is_doublecheck():
        doublecheck_who = drug.get_doublecheck_who()
        doublecheck_when = drug.get_doublecheck_when()

    context = {
        'drug': drug,
        'lastmod': lastmod,
        'lastmod_who': lastmod_who,
        'lastmod_when': lastmod_when,
        'doublecheck': doublecheck,
        'doublecheck_who': doublecheck_who,
        'doublecheck_when': doublecheck_when,
    }
    return render(request, 'drug_detail.html', context)


@login_required
def DrugAddView(request):
    """ Add New Drug object """

    if request.method == "POST":
        form = DrugForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            user = get_request().user
            obj_type = DRUG
            msg = "Medicijn is toegevoegd"
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            log_addition(user, p, obj_type, msg)
            return redirect('drug-detail', pk=p.pk)
    else:
        form = DrugForm()
        context = {
            'form': form,
        }
        return render(request, 'drug_add.html', context)


@login_required
def DrugEditView(request, pk):
    """ Edit view of Drug object """

    try:
        drug = Drug.objects.get(pk=pk)
    except Drug.DoesNotExist:
        raise Http404("drug does not exist")

    if request.method == "POST":
        form = DrugForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)

            if not p.pk:
                p.pk = drug.pk
            if not p.created:
                p.created = drug.created

            user = get_request().user
            obj_type = DRUG
            if p.doublecheck:
                p.doublecheck = False
                msg = "Medicijn %s is aangepast; dubbelcontrole vlag verwijderd" % drug.name
            else:
                msg = "Medicijn %s is aangepast" % drug.name
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            log_change(user, drug, obj_type, msg)
            return redirect('drug-detail', pk=p.pk)
    else:
        drug_initial_data = {
            'name': drug.name,
            'ingredient': drug.ingredient,
            'use': drug.use,
            'sideeffects': drug.sideeffects,
            'particularities': drug.particularities,
            'appearance': drug.appearance,
            'intake': drug.intake,
        }
        form = DrugForm(initial=drug_initial_data)
        context = {
            'form': form,
            'drug': drug,
        }
        return render(request, 'drug_edit.html', context)


@login_required
def ClientListView(request):
    """ Client List view (paginated) """

    client_list = Client.objects.order_by('lastname')
    paginator = Paginator(client_list, 15)
    page = request.GET.get('page')
    try:
        plist = paginator.get_page(page)
    except PageNotAnInteger:
        plist = paginator.get_page(1)
    except EmptyPage:
        plist = paginator.get_page(paginator.num_pages)

    context = {'plist': plist}
    return render(request, 'client_index.html', context)


@login_required
def ClientDoublecheckView(request, pk):
    """ Doublecheck view of Client object """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404("client does not exist")

    lastmod_who = 'Unknown'
    if client.is_lastmod():
        lastmod_who = client.get_lastmod_who()
    request_who = get_request().user
    context = {
        'client': client,
        'lastmod_who': lastmod_who,
        'request_who': request_who,
    }
    return render(request, 'client_doublecheck.html', context)


@login_required
def ClientDoublecheckNextView(request, pk):
    """ DoublecheckNext view of Client object """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404("client does not exist")

    user = get_request().user
    obj_type = CLIENT
    msg = "Client %s is dubbelgecontroleerd" % client.firstname
    client.doublecheck = True
    client.doublecheck_who = get_request().user
    client.doublecheck_when = timezone.now()
    client.save()
    log_doublecheck(user, client, obj_type, msg)
    return redirect('client-detail', pk=client.pk)

@login_required
def ClientDetailView(request, pk):
    """ Detail view (index) or Client object """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404("client does not exist")

    client_plist = Prescription.objects.filter(client__id=pk)

    lastmod = client.is_lastmod()
    doublecheck = client.is_doublecheck()
    lastmod_who = ''
    lastmod_when = ''
    doublecheck_who = ''
    doublecheck_when = ''
    if client.is_lastmod():
        lastmod_who = client.get_lastmod_who()
        lastmod_when = client.get_lastmod_when()
    if client.is_doublecheck():
        doublecheck_who = client.get_doublecheck_who()
        doublecheck_when = client.get_doublecheck_when()

    context = {
        'client': client,
        'lastmod': lastmod,
        'lastmod_who': lastmod_who,
        'lastmod_when': lastmod_when,
        'doublecheck': doublecheck,
        'doublecheck_who': doublecheck_who,
        'doublecheck_when': doublecheck_when,
        'client_plist': client_plist,
    }
    return render(request, 'client_detail.html', context)


@login_required
def ClientAddView(request):
    """ Add New Client object """

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            user = get_request().user
            obj_type = CLIENT
            msg = "Client is toegevoegd"
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            log_addition(user, p, obj_type, msg)
            return redirect('client-detail', pk=p.pk)
        else:
            messages.error(request, "Error: form not valid")
    else:
        form = ClientForm()
        context = {
            'form': form,
        }
        return render(request, 'client_add.html', context)


@login_required
def ClientEditView(request, pk):
    """ Edit view of Client object """

    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404("client does not exist")

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)

            if not p.pk:
                p.pk = client.pk
            if not p.created:
                p.created = client.created

            user = get_request().user
            obj_type = CLIENT
            if p.doublecheck:
                p.doublecheck = False
                msg = "Client %s %s is aangepast; dubbelcontrole vlag verwijderd" % (
                    client.firstname,
                    client.lastname)
            else:
                msg = "Client %s %s is aangepast" % (
                    client.firstname,
                    client.lastname)
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            log_change(user, client, obj_type, msg)
            return redirect('client-detail', pk=p.pk)
    else:
        client_initial_data = {
            'firstname': client.firstname,
            'lastname': client.lastname,
            'dateofbirth': client.dateofbirth,
            'bsn': client.bsn,
        }
        form = ClientForm(initial=client_initial_data)
        context = {
            'form': form,
            'client': client,
        }
        return render(request, 'client_edit.html', context)


@login_required
def PrescriptionListView(request):
    """ List view (index) or Prescription objects """

    prescription_list = Prescription.objects.order_by('-created')
    paginator = Paginator(prescription_list, 15)
    page = request.GET.get('page')
    try:
        plist = paginator.get_page(page)
    except PageNotAnInteger:
        plist = paginator.get_page(1)
    except EmptyPage:
        plist = paginator.get_page(paginator.num_pages)

    context = {'plist': plist}
    return render(request, 'prescription_index.html', context)


@login_required
def PrescriptionDoublecheckView(request, pk):
    """ Doublecheck view of Drug object """
    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("prescription does not exist")

    lastmod_who = 'Unknown'
    if prescription.is_lastmod():
        lastmod_who = prescription.get_lastmod_who()
    request_who = get_request().user
    context = {
        'prescription': prescription,
        'lastmod_who': lastmod_who,
        'request_who': request_who,
    }
    return render(request, 'prescription_doublecheck.html', context)


@login_required
def PrescriptionDoublecheckNextView(request, pk):
    """ DoublecheckNext view of Drug object """
    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("prescription does not exist")

    user = get_request().user
    obj_type = PRESCRIPTION
    msg = "Prescriptie %s is dubbelgecontroleerd" % prescription.name
    prescription.doublecheck = True
    prescription.doublecheck_who = get_request().user
    prescription.doublecheck_when = timezone.now()
    prescription.save()
    log_doublecheck(user, prescription, obj_type, msg)
    return redirect('prescription-detail', pk=prescription.pk)


@login_required
def PrescriptionDetailView(request, pk):
    """ Detail view (index) or Prescription object """

    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("Prescription does not exist")

    lastmod = prescription.is_lastmod()
    lastmod_who = ''
    lastmod_when = ''
    doublecheck = prescription.is_doublecheck()
    doublecheck_who = ''
    doublecheck_when = ''
    if prescription.is_lastmod():
        lastmod_who = prescription.get_lastmod_who()
        lastmod_when = prescription.get_lastmod_when()
    if prescription.is_doublecheck():
        doublecheck_who = prescription.get_doublecheck_who()
        doublecheck_when = prescription.get_doublecheck_when()

    context = {
        'prescription': prescription,
        'lastmod': lastmod,
        'lastmod_who': lastmod_who,
        'lastmod_when': lastmod_when,
        'doublecheck': doublecheck,
        'doublecheck_who': doublecheck_who,
        'doublecheck_when': doublecheck_when,
    }
    return render(request, 'prescription_detail.html', context)


@login_required
def PrescriptionEditView(request, pk):
    """ Edit view (index) of Prescription object """

    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("prescription does not exist")

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)

            if not p.pk:
                p.pk = prescription.pk
            if not p.created:
                p.created = prescription.created
            if not p.matrix:
                p.matrix = prescription.matrix

            p.m_d00100_p00100 = prescription.m_d00100_p00100
            p.m_d00200_p00100 = prescription.m_d00200_p00100
            p.m_d00300_p00100 = prescription.m_d00300_p00100
            p.m_d00400_p00100 = prescription.m_d00400_p00100
            p.m_d00500_p00100 = prescription.m_d00500_p00100
            p.m_d00600_p00100 = prescription.m_d00600_p00100
            p.m_d00700_p00100 = prescription.m_d00700_p00100
            p.m_d00100_p00200 = prescription.m_d00100_p00200
            p.m_d00200_p00200 = prescription.m_d00200_p00200
            p.m_d00300_p00200 = prescription.m_d00300_p00200
            p.m_d00400_p00200 = prescription.m_d00400_p00200
            p.m_d00500_p00200 = prescription.m_d00500_p00200
            p.m_d00600_p00200 = prescription.m_d00600_p00200
            p.m_d00700_p00200 = prescription.m_d00700_p00200
            p.m_d00100_p00300 = prescription.m_d00100_p00300
            p.m_d00200_p00300 = prescription.m_d00200_p00300
            p.m_d00300_p00300 = prescription.m_d00300_p00300
            p.m_d00400_p00300 = prescription.m_d00400_p00300
            p.m_d00500_p00300 = prescription.m_d00500_p00300
            p.m_d00600_p00300 = prescription.m_d00600_p00300
            p.m_d00700_p00300 = prescription.m_d00700_p00300
            p.m_d00100_p00400 = prescription.m_d00100_p00400
            p.m_d00200_p00400 = prescription.m_d00200_p00400
            p.m_d00300_p00400 = prescription.m_d00300_p00400
            p.m_d00400_p00400 = prescription.m_d00400_p00400
            p.m_d00500_p00400 = prescription.m_d00500_p00400
            p.m_d00600_p00400 = prescription.m_d00600_p00400
            p.m_d00700_p00400 = prescription.m_d00700_p00400
            p.m_d00100_p00500 = prescription.m_d00100_p00500
            p.m_d00200_p00500 = prescription.m_d00200_p00500
            p.m_d00300_p00500 = prescription.m_d00300_p00500
            p.m_d00400_p00500 = prescription.m_d00400_p00500
            p.m_d00500_p00500 = prescription.m_d00500_p00500
            p.m_d00600_p00500 = prescription.m_d00600_p00500
            p.m_d00700_p00500 = prescription.m_d00700_p00500

            user = get_request().user
            obj_type = PRESCRIPTION
            if p.doublecheck:
                p.doublecheck = False
                msg = "Prescriptie %s aangepast, \
                    dubbelcontrole vlag verwijderd" % prescription.name
            else:
                msg = "Prescriptie %s aangepast" % prescription.name
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            update_pe(p.pk)
            log_change(user, prescription, obj_type, msg)
            return redirect('prescription-detail', pk=p.pk)
        else:
            messages.error(request, "Error: form not valid")
    else:
        prescription_initial_data = {
            'name': prescription.name,
            'client': prescription.client,
            'drug': prescription.drug,
            'doctor': prescription.doctor,
            'start_date': prescription.start_date,
            'end_date': prescription.end_date,
            'remarks': prescription.remarks,
        }
        form = PrescriptionForm(initial=prescription_initial_data)
        context = {
            'form': form,
            'prescription': prescription,
        }
    return render(request, 'prescription_edit.html', context)


@login_required
def PrescriptionMatrixEditView(request, pk):
    """ Edit view (index) of Prescription object """
    try:
        prescription = Prescription.objects.get(pk=pk)
    except Prescription.DoesNotExist:
        raise Http404("prescription does not exist")

    if request.method == "POST":
        form = PrescriptionMatrixForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)

            if not p.pk:
                p.pk = prescription.pk
            if not p.created:
                p.created = prescription.created
            if not p.name:
                p.name = prescription.name
            if not p.client_id:
                p.client_id = prescription.client_id
            if not p.doctor_id:
                p.doctor_id = prescription.doctor_id
            if not p.drug_id:
                p.drug_id = prescription.drug_id
            if not p.start_date:
                p.start_date = prescription.start_date
            if not p.end_date:
                p.end_date = prescription.end_date
            if not p.remarks:
                p.remarks = prescription.remarks

            user = get_request().user
            obj_type = PRESCRIPTION
            if p.doublecheck:
                p.doublecheck = False
                msg = "Prescriptie matrix %s aangepast, \
                    dubbelcontrole vlag verwijderd" % prescription.name
            else:
                msg = "Prescriptie matrix %s aangepast" % prescription.name
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.matrix = True
            p.save()
            update_pe(p.pk)
            log_change(user, prescription, obj_type, msg)
            return redirect('prescription-detail', pk=p.pk)
        else:
            messages.error(request, "Error: form not valid")

    else:
        prescription_matrix_initial_data = {
            'name': prescription.name,
            'client': prescription.client,
            'drug': prescription.drug,
            'doctor': prescription.doctor,
            'start_date': prescription.start_date,
            'end_date': prescription.end_date,
            'm_d00100_p00100': prescription.m_d00100_p00100,
            'm_d00200_p00100': prescription.m_d00200_p00100,
            'm_d00300_p00100': prescription.m_d00300_p00100,
            'm_d00400_p00100': prescription.m_d00400_p00100,
            'm_d00500_p00100': prescription.m_d00500_p00100,
            'm_d00600_p00100': prescription.m_d00600_p00100,
            'm_d00700_p00100': prescription.m_d00700_p00100,
            'm_d00100_p00200': prescription.m_d00100_p00200,
            'm_d00200_p00200': prescription.m_d00200_p00200,
            'm_d00300_p00200': prescription.m_d00300_p00200,
            'm_d00400_p00200': prescription.m_d00400_p00200,
            'm_d00500_p00200': prescription.m_d00500_p00200,
            'm_d00600_p00200': prescription.m_d00600_p00200,
            'm_d00700_p00200': prescription.m_d00700_p00200,
            'm_d00100_p00300': prescription.m_d00100_p00300,
            'm_d00200_p00300': prescription.m_d00200_p00300,
            'm_d00300_p00300': prescription.m_d00300_p00300,
            'm_d00400_p00300': prescription.m_d00400_p00300,
            'm_d00500_p00300': prescription.m_d00500_p00300,
            'm_d00600_p00300': prescription.m_d00600_p00300,
            'm_d00700_p00300': prescription.m_d00700_p00300,
            'm_d00100_p00400': prescription.m_d00100_p00400,
            'm_d00200_p00400': prescription.m_d00200_p00400,
            'm_d00300_p00400': prescription.m_d00300_p00400,
            'm_d00400_p00400': prescription.m_d00400_p00400,
            'm_d00500_p00400': prescription.m_d00500_p00400,
            'm_d00600_p00400': prescription.m_d00600_p00400,
            'm_d00700_p00400': prescription.m_d00700_p00400,
            'm_d00100_p00500': prescription.m_d00100_p00500,
            'm_d00200_p00500': prescription.m_d00200_p00500,
            'm_d00300_p00500': prescription.m_d00300_p00500,
            'm_d00400_p00500': prescription.m_d00400_p00500,
            'm_d00500_p00500': prescription.m_d00500_p00500,
            'm_d00600_p00500': prescription.m_d00600_p00500,
            'm_d00700_p00500': prescription.m_d00700_p00500,
        }

        form = PrescriptionMatrixForm(initial=prescription_matrix_initial_data)
        context = {
            'form': form,
            'prescription': prescription,
        }
        return render(request, 'prescription_matrix_edit.html', context)


@login_required
def PrescriptionAddView(request):
    """ Add New Prescription object """

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            user = get_request().user
            obj_type = PRESCRIPTION
            msg = "Prescriptie is toegevoegd"
            p.lastmod = True
            p.lastmod_who = get_request().user
            p.lastmod_when = timezone.now()
            p.save()
            create_pe(p.pk)
            log_addition(user, p, obj_type, msg)
            return redirect('prescription-detail', pk=p.pk)
        else:
            messages.error(request, "Error: form not valid")

    else:
        form = PrescriptionForm()
        context = {
            'form': form,
        }
        return render(request, 'prescription_add.html', context)
