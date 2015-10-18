"""
Interface for the IP2Location DB5 database.

URL: http://lite.ip2location.com/database-ip-country-region-city-latitude-longitude

Uses ``IP2Location`` from IP2Location: http://www.ip2location.com/developers/python
Requires the BIN DB5 database to be locally available.
"""
import ipaddress
from django.contrib.gis.geos import Point
from django.utils.datetime_safe import datetime
from geodb.interfaces import GeoIPInterface
from IP2Location import IP2Location as IP2LocationReader


class IP2Location(GeoIPInterface):
    """
    Interface for the IP2Location DB5 database.
    """
    name = "IP2Location DB5.LITE"
    codename = "ip2location"
    url = "http://lite.ip2location.com/database-ip-country-region-city-latitude-longitude"
    license = "This product includes IP2Location LITE data available from " \
              "<a href=\"http://www.ip2location.com\">http://www.ip2location.com</a>."

    def get_version(self):
        reader = self._get_reader_v4()
        return datetime(year=reader._dbyear + 2000, month=reader._dbmonth,
                        day=reader._dbday).strftime('%Y-%m-%d')

    def query_v4(self, address: ipaddress.IPv4Address) -> Point:
        reader = self._get_reader_v4()
        result = reader.get_all(str(address))

        if result:
            return Point(result.latitude, result.longitude)
        return None

    def query_v6(self, address: ipaddress.IPv6Address) -> Point:
        reader = self._get_reader_v6()
        result = reader.get_all(str(address))

        if result:
            return Point(result.latitude, result.longitude)
        return None

    def _get_reader_v4(self):
        return IP2LocationReader(self._get_file('ip2location/IP2LOCATION-LITE-DB5.BIN'))

    def _get_reader_v6(self):
        return IP2LocationReader(self._get_file('ip2location/IP2LOCATION-LITE-DB5.IPV6.BIN'))


interface = IP2Location
