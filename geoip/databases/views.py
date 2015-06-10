"""
Views for the GeoIP databases app.
"""
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.databases.models import Database


class DatabaseListView(ListView):
    """
    Lists active databases.
    """
    queryset = Database.objects.all()
    context_object_name = 'databases'


class DatabaseDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows an active database.
    """
    queryset = Database.objects.all()
    context_object_name = 'database'
