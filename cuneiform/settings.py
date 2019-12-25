"""
Django settings for core project.
"""

import os
from .secret_settings import SECRET_SECRET_KEY, SECRET_DATABASES, SECRET_USE_TZ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = SECRET_SECRET_KEY
DATABASES = SECRET_DATABASES

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'h2858779.stratoserver.net', 'cuneiform.healthcare']

# Application definition
INSTALLED_APPS = [
    'medslist.apps.MedslistConfig',
    'signoff.apps.SignoffConfig',
    'report.apps.ReportConfig',
    'log.apps.LogConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'crispy_forms',
    'octicons',
    'simple_history',
    'organizations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'audit_log.middleware.UserLoggingMiddleware',
    'medslist.get_current_user.RequestMiddleware',
]

ROOT_URLCONF = 'cuneiform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'cuneiform', 'templates'),
            os.path.join(BASE_DIR, 'templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cuneiform.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'nl'
TIME_ZONE = 'Europe/Amsterdam'
USE_I18N = True
USE_L10N = True
USE_TZ = SECRET_USE_TZ

# Static files (CSS, JavaScript, Images)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/medslist'
LOGOUT_REDIRECT_URL = '/medslist'

CUNEIFORM_VERSION = '0.2.0'
CUNEIFORM_COLOR_1 = 'lightblue'
CUNEIFORM_COLOR_2 = 'grey'

SOUTH_TESTS_MIGRATE = False
