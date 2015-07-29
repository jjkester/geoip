"""
Django Admin configuration for the GeoIP results app.
"""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import ugettext_lazy as _
from geoip.measurements.admin_actions import run_measurements
from geoip.measurements.models import Dataset, Measurement


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the Dataset model.
    """
    actions = (run_measurements,)
    fieldsets = (
        (None, {
            'fields': ('start', 'end', 'notes', 'status'),
        }),
        (_("Advanced options"), {
            'classes': 'collapse',
            'fields': ('is_public', 'created'),
        }),
    )
    list_display = ('__str__', 'start', 'end', 'is_public')
    list_display_links = ('__str__',)
    list_filter = ('is_public',)
    readonly_fields = ('status', 'created')


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
            'fields': ('ipv4_location', 'ipv6_location', 'ipv4_distance', 'ipv6_distance', 'mutual_distance'),
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