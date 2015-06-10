"""
Data models for investigated nodes in the GeoIP project.
"""
from django.contrib.gis.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from hashids import Hashids


class NodeQuerySet(models.QuerySet):
    """
    Custom QuerySet for Node objects.
    """
    def active(self):
        """Returns active nodes."""
        return self.filter(is_active=True)

    def usable(self):
        """Returns usable nodes. This are nodes with a location and at least one IP address."""
        return self.exclude(location=None).exclude(Q(ipv4=None) | Q(ipv6=None))


class Node(models.Model):
    """
    Represents a physical computer system with a known location. A system can have multiple IP addresses.
    """
    name = models.CharField(max_length=255, verbose_name=_("name"))
    dns_name = models.CharField(blank=True, max_length=255, verbose_name=_("domain name"))
    source = models.ForeignKey('DataSource', on_delete=models.PROTECT, related_name='nodes', verbose_name=_("source"))
    notes = models.TextField(blank=True, verbose_name=_("notes"))
    location = models.PointField(blank=True, null=True, geography=True, verbose_name=_("known location"))
    ipv4 = models.GenericIPAddressField(blank=True, null=True, protocol='ipv4', verbose_name=_("IPv4 address"))
    ipv6 = models.GenericIPAddressField(blank=True, null=True, protocol='ipv6', verbose_name=_("IPv6 address"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("last updated"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    # Manager
    objects = NodeQuerySet.as_manager()

    # HashIDs
    hashids = Hashids(salt='N0d3', min_length=5)

    class Meta:
        verbose_name = _("node")
        verbose_name_plural = _("nodes")

    def __str__(self):
        return "{name:s}".format(name=self.name)

    @cached_property
    def hashid(self):
        return self.hashids.encode(self.id)


class DataSource(models.Model):
    """
    A source for data used in the application. Sources should be used to make verifying the data possible.
    """
    name = models.CharField(max_length=200, verbose_name=_("name"))
    url = models.URLField(verbose_name=_("URL"))

    class Meta:
        ordering = ['name']
        verbose_name = _("source")
        verbose_name_plural = _("sources")

    def __str__(self):
        return "{name:s}. {url:s}".format(
            name=self.name,
            url=self.url,
        )
