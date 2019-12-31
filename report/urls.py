from django.urls import path
#from django.conf.urls import url
from django_filters.views import FilterView
from .filters import PeFilter, PeFilterSignoff
from . import views

urlpatterns = [
    path('', views.index, name='report-index'),
    path('report/overview/pe/', FilterView.as_view(filterset_class=PeFilter,
        template_name='report_overview_pe.html'), name='report-overview-pe'),
    path('report/overview/pe/signoff', FilterView.as_view(filterset_class=PeFilterSignoff,
        template_name='report_overview_pe_signoff.html'), name='report-overview-pe-signoff'),
    path('report/overview/notsignedoff/',
        views.ReportOverviewTodayNotsignedoff, name='report-overview-today-notsignedoff'),
]
