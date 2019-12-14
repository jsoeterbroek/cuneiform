from django.urls import path
#from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='medslist-index'),
    path('prescription/', views.PrescriptionListView, name='prescription'),
    path('prescription/add/', views.PrescriptionAddView, name='prescription-add'),
    path('prescription/<int:pk>/', views.PrescriptionDetailView, name='prescription-detail'),
    path('prescription/<int:pk>/edit/', views.PrescriptionEditView, name='prescription-edit'),
    path('prescription/<int:pk>/doublecheck/', views.PrescriptionDoublecheckView, name='prescription-doublecheck'),
    path('prescription/<int:pk>/doublechecknext/', views.PrescriptionDoublecheckNextView, name='prescription-doublecheck-next'),
    path('client/', views.ClientListView, name='client'),
    path('client/add/', views.ClientAddView, name='client-add'),
    path('client/<int:pk>/', views.ClientDetailView, name='client-detail'),
    path('client/<int:pk>/edit/', views.ClientEditView, name='client-edit'),
    path('client/<int:pk>/doublecheck/', views.ClientDoublecheckView, name='client-doublecheck'),
    path('client/<int:pk>/doublechecknext/', views.ClientDoublecheckNextView, name='client-doublecheck-next'),
    path('log/', views.LogListView, name='log'),
    path('overview/doublecheck/', views.OverviewDoublecheckListView, name='overview-doublecheck'),
    path('drug/', views.DrugListView, name='drug'),
    path('drug/add/', views.DrugAddView, name='drug-add'),
    path('drug/<int:pk>/', views.DrugDetailView, name='drug-detail'),
    path('drug/<int:pk>/edit/', views.DrugEditView, name='drug-edit'),
    path('drug/<int:pk>/doublecheck/', views.DrugDoublecheckView, name='drug-doublecheck'),
    path('drug/<int:pk>/doublechecknext/', views.DrugDoublecheckNextView, name='drug-doublecheck-next'),
]
