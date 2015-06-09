"""
Django Admin configuration for the GeoIP databases app.
"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from geoip.databases.models import Database


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the Database model.
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'version', 'url', 'notes'),
        }),
        (_("Advanced options"), {
            'classes': 'collapse',
            'fields': ('codename', 'is_active'),
        }),
    )
    list_display = ('name', 'version', 'codename', 'is_active')
    list_display_links = ('name', 'version')
    list_filter = ('is_active',)
    readonly_fields = ('codename',)
    search_fields = ('name', 'codename')
