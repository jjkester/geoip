"""
Data models for the results of the measurements of the GeoIP application.
"""
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids
from geoip.contrib.choices import Choice


class Dataset(models.Model):
    """
    Represents a single result set.
    """
    class Status(Choice):
        queued = (0, _("queued"))
        running = (1, _("running"))
        success = (2, _("success"))
        error = (-1, _("error"))

    start = models.DateTimeField(blank=True, verbose_name=_("start time"))
    end = models.DateTimeField(blank=True, verbose_name=_("end time"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    status = models.SmallIntegerField(choices=Status.choices(), default=Status.queued.value, verbose_name=_("status"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    is_public = models.BooleanField(default=False, verbose_name=_("is public"))

    # HashIDs
    hashids = Hashids(salt='D474S37', min_length=5)

    class Meta:
        get_latest_by = 'start'
        ordering = ['start']
        verbose_name = _("data set")
        verbose_name_plural = _("data sets")

    def __str__(self):
        return "{identifier:s} ({date:s})".format(
            identifier=self.hashids.encode(self.id),
            date=self.start.strftime('%Y-%m-%d'),
        )


class Measurement(models.Model):
    """
    Result of a location measurement. Contains the location of one IP address according to one database.
    """
    node = models.ForeignKey('nodes.Node', on_delete=models.PROTECT, related_name='measurements',
                             verbose_name=_("node"))
    dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='measurements',
                                verbose_name=_("data set"))
    database = models.ForeignKey('databases.Database', on_delete=models.PROTECT, related_name='measurements',
                                 verbose_name=_("GeoIP database"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    ipv4_location = models.PointField(geography=True, verbose_name=_("IPv4 location"))
    ipv6_location = models.PointField(geography=True, verbose_name=_("IPv6 location"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))

    # Manager
    objects = models.GeoManager()

    # HashIDs
    hashids = Hashids(salt='m3a5ur3m3n7', min_length=12)

    class Meta:
        ordering = ['dataset', 'database', 'created']
        verbose_name = _("measurement")
        verbose_name_plural = _("measurements")

    def __str__(self):
        return "{verbose_name:s} {identifier:s}".format(
            verbose_name=self._meta.verbose_name.capitalize(),
            identifier=self.hashids.encode(self.id),
        )
