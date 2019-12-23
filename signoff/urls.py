from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='signoff-index'),
    path('today/', views.SignoffToday, name='signoff-today'),
    path('today/period/<str:period>/',
         views.SignoffTodayPeriod, name='signoff-today-period'),
    path('today/pe/<str:pe_id>/',
         views.SignoffTodayPe, name='signoff-today-pe'),
    path('today/period/<str:period>/client/<int:client_id>/submit/',
         views.SignoffTodayPeriodClientSubmit, name='signoff-today-period-client-submit'),
    path('today/overview/notsignedoff/',
         views.SignoffOverviewTodayNotsignedoff, name='signoff-overview-today-notsignedoff'),
    path('client/', views.SignoffClient, name='signoff-client'),
    path('client/<int:client_id>/', views.SignoffClient, name='signoff-client-id'),
]
