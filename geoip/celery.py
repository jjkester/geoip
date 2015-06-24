"""
Celery configuration for the GeoIP application.
"""
from __future__ import absolute_import
from celery import Celery
import os

# Set default Django settings module for Celery programs
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoip.settings')

# Import settings after setting the settings module
from django.conf import settings

app = Celery('geoip')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
