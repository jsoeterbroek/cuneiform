"""cuneiform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
#from organizations.backends import invitation_backend
from . import views

urlpatterns = [
    path('', views.MainIndexView, name='main-index'),
    path('license/', views.LicenseView, name='license'),
    path('feedback/', views.FeedbackView, name='feedback'),
    path('versie/', views.VersieView, name='versie'),
    path('info/', views.InfoView, name='info'),
    path('medslist/', include('medslist.urls'), name='medslist-index'),
    path('signoff/', include('signoff.urls'), name='signoff-index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/<int:pk>/', views.UserProfileView, name='user-profile'),
    url(r'^accounts/', include('organizations.urls')),
]
