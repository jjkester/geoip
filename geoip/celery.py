"""
Celery configuration for the GeoIP application.
"""
from __future__ import absolute_import
from celery import Celery, task
import os

# Set default Django settings module for Celery programs
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoip.settings')

# Import settings after setting the settings module
from django.conf import settings

app = Celery('geoip')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Set generic task
@task()
def run_management_command(command, *args, **kwargs):
    return call_command(command, *args, **kwargs)
