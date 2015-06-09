"""
Data models for GeoIP databases.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids


class Database(models.Model):
    """
    Represents a GeoIP database that is queried by the GeoIP application.
    """
    codename = models.CharField(max_length=255, unique=True, verbose_name=_("code name"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    version = models.CharField(max_length=255, verbose_name=_("version"))
    url = models.URLField(blank=True, verbose_name=_("website"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    # HashIDs
    hashids = Hashids(salt='d47484S3', min_length=5)

    class Meta:
        ordering = ['-is_active', 'name']
        verbose_name = _("GeoIP database")
        verbose_name_plural = _("GeoIP databases")

    def __str__(self):
        return "{name:s} ({version:s})".format(
            name=self.name,
            version=self.version,
        )
