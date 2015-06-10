"""
Common interface for different GeoIP databases.
"""
import ipaddress
import os
from django.conf import settings
from django.contrib.gis.geos import Point
from geoip.databases.models import Database


class GeoIPInterface(object):
    """
    Common interface for GeoIP databases.
    """
    name = ""
    codename = ""
    url = ""
    license = ""

    def __init__(self):
        pass

    def query(self, address: str) -> Point:
        """
        Query the database for the given IP address.
        :param address: The IP address to find the location for.
        :type address: str
        :return: The location of the IP address or ``None`` if not known.
        :rtype: Point
        """
        ip_address = ipaddress.ip_address(address)
        query_method = getattr(self, 'query_v{0:d}'.format(ip_address.version))

        if not query_method:
            raise NotImplementedError(
                "Database {name:s} does not support querying IPv{v:d} addresses.".format(name=self.name,
                                                                                         v=ip_address.version))
        return query_method(ip_address)

    def query_v4(self, address: ipaddress.IPv4Address) -> Point:
        """
        Query the database for the given IPv4 address.
        :param address: The IPv4 address to find the location for.
        :type address: ipaddress.IPv4Address
        :return: The location of the IP address or ``None`` if not known.
        :rtype: Point
        """
        raise NotImplementedError("Database {name:s} does not support querying IPv4 addresses.".format(name=self.name))

    def query_v6(self, address: ipaddress.IPv6Address) -> Point:
        """
        Query the database for the given IPv6 address.
        :param address: The IPv6 address to find the location for.
        :type address: ipaddress.IPv6Address
        :return: The location of the IP address or ``None`` if not known.
        :rtype: Point
        """
        raise NotImplementedError("Database {name:s} does not support querying IPv6 addresses.".format(name=self.name))

    def close(self):
        """
        Called when the interface is no longer needed.
        """
        pass

    def get_version(self):
        """
        :return: The current version of the database.
        """
        return ""

    def _get_storage_root(self):
        """
        :return: The folder containing GeoIP database files.
        """
        return getattr(settings, 'GEOIP_DATABASES_FOLDER',
                       os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'databases'))

    def _get_file(self, *paths: str) -> str:
        """
        :return: The path to the given file.
        """
        return os.path.join(self._get_storage_root(), *paths)
