"""
Django Admin configuration for the GeoIP results app.
"""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import ugettext_lazy as _
from geoip.results.models import Dataset, Measurement


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the Dataset model.
    """
    fieldsets = (
        (None, {
            'fields': ('start', 'end', 'notes',),
        }),
        (_("Advanced options"), {
            'classes': 'collapse',
            'fields': ('is_public', 'created'),
        }),
    )
    list_display = ('__str__', 'start', 'end', 'is_public')
    list_display_links = ('__str__',)
    list_filter = ('is_public',)
    readonly_fields = ('created',)


@admin.register(Measurement)
class MeasurementAdmin(OSMGeoAdmin):
    """
    Django Admin configuration for the Measurement model.
    """
    fieldsets = (
        (None, {
            'fields': ('node', 'dataset', 'database', 'notes'),
        }),
        (_("Measurement data"), {
            'classes': 'collapse',
            'fields': ('ipv4_location', 'ipv6_location'),
        }),
        (_("Advanced options"), {
            'classes': 'collapse',
            'fields': ('created',),
        }),
    )
    list_display = ('__str__', 'dataset', 'node', 'database')
    list_display_links = ('__str__',)
    list_filter = ('dataset', 'database')
    raw_id_fields = ('node', 'dataset')
    readonly_fields = ('created',)
    search_fields = ('node__name', 'node__dns_name')