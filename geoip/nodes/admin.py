"""
Django Admin configuration for the GeoIP nodes app.
"""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.translation import ugettext_lazy as _
from geoip.nodes.models import Node, DataSource


@admin.register(Node)
class NodeAdmin(OSMGeoAdmin):
    """
    Django Admin configuration for the Node model.
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'dns_name', 'source', 'notes'),
        }),
        (_("Measurement options"), {
            'classes': 'collapse',
            'fields': ('location', 'ipv4', 'ipv6'),
        }),
        (_("Advanced options"), {
            'classes': 'collapse',
            'fields': ('is_active', 'last_updated', 'created'),
        }),
    )
    list_display = ('name', 'dns_name', 'location', 'source', 'is_active')
    list_display_links = ('name', 'dns_name')
    list_filter = ('source', 'is_active')
    readonly_fields = ('last_updated', 'created')
    search_fields = ('name', 'dns_name', 'location')


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the DataSource model.
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'url'),
        }),
    )
    list_display = ('name', 'url')
    list_display_links = ('name',)
    search_fields = ('name', 'url')
