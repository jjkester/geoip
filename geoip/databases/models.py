"""
Data models for GeoIP databases.
"""
from django.core.validators import validate_slug
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids


class DatabaseQuerySet(models.QuerySet):
    """
    Custom query set of Database objects.
    """
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Database(models.Model):
    """
    Represents a GeoIP database that is queried by the GeoIP application.
    """
    codename = models.CharField(max_length=255, unique=True, validators=[validate_slug], verbose_name=_("code name"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    version = models.CharField(max_length=255, verbose_name=_("version"))
    url = models.URLField(blank=True, verbose_name=_("website"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    # HashIDs
    hashids = Hashids(salt='d47484S3', min_length=5)

    # Manager
    objects = DatabaseQuerySet.as_manager()

    class Meta:
        ordering = ['-is_active', 'name']
        verbose_name = _("GeoIP database")
        verbose_name_plural = _("GeoIP databases")

    def __str__(self):
        return "{name:s} ({version:s})".format(
            name=self.name,
            version=self.version,
        )

    @cached_property
    def hashid(self):
        return self.hashids.encode(self.id)
