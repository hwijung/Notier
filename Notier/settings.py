"""
Django settings for Notier project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# celery settings 
from __future__ import absolute_import
from celery import Celery
from django.conf import settings
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'spmlrxsz#2uie1%8-9sn%tp!0lpf9m*##x3h3)!7fjte%#)2=='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'alarm',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Notier.urls'

WSGI_APPLICATION = 'Notier.wsgi.application'

# Celery
app = Celery('Notier', broker='amqp://', backend='amqp://', include=['alarm.tasks'])
app.conf.update(
                BROKER_URL = 'amqp://',
                CELERY_RESULT_BACKEND = 'amqp://',                
                CELERY_TASK_SERIALIZER = 'json',
                CELERY_RESULT_SERIALIZER = 'json',
                CELERY_ACCEPT_CONTENT=['json'],  
                CELERY_TIMEZONE = 'Asia/Seoul',
                CELERY_ENABLE_UTC = True,
                CELERYD_CONCURRENCY = 1,
                CELERYBEAT_SCHEDULE = {
                    'runs-every-minutes': {
                        'task':'alarm.tasks.test',
                        'schedule':timedelta(seconds=60)
                        }
})                      
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login/'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]
