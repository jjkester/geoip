"""
Interface for the MaxMind GeoLite2 GeoIP database.

URL: http://dev.maxmind.com/geoip/geoip2/geolite2/

Uses ``geoip2`` from MaxMind: https://github.com/maxmind/GeoIP2-python
Requires the C API (https://github.com/maxmind/libmaxminddb) to be installed and the database to be available locally.
"""
import ipaddress
from django.contrib.gis.geos import Point
from geoip2 import database
from geoip2.errors import AddressNotFoundError
from geoip_databases.interfaces import GeoIPInterface


class GeoLite2(GeoIPInterface):
    """
    Interface for the MaxMind GeoLite2 GeoIP database.
    """
    name = "MaxMind GeoLite2"
    codename = "geolite2"
    url = "http://dev.maxmind.com/geoip/geoip2/geolite2/"
    license = "This product includes GeoLite2 data created by MaxMind, available from " \
              "<a href=\"http://www.maxmind.com\">http://www.maxmind.com</a>."

    def __init__(self):
        super().__init__()
        self._reader = self._get_reader()

    def close(self):
        self._reader.close()

    def get_version(self):
        return str(self._reader.metadata().build_epoch)

    def query_v4(self, address: ipaddress.IPv4Address) -> Point:
        try:
            response = self._reader.city(str(address))
            return Point(
                response.location.latitude,
                response.location.longitude,
                srid=4326,
            )
        except AddressNotFoundError:
            return None

    def query_v6(self, address: ipaddress.IPv6Address) -> Point:
        pass

    def _get_reader(self):
        return database.Reader(self._get_file('geolite2/GeoLite2-City.mmdb'))


interface = GeoLite2
