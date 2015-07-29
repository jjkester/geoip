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
    license = "This product includes IP2Location LITE data available from" \
              "<a href=\"http://www.ip2location.com\">http://www.ip2location.com</a>."

    def __init__(self):
        super().__init__()
        self._reader = self._get_reader()

    def get_version(self):
        return datetime(year=self._reader._dbyear + 2000, month=self._reader._dbmonth,
                        day=self._reader._dbday).strftime('%Y-%m-%d')

    def query_v4(self, address: ipaddress.IPv4Address) -> Point:
        return self._query(str(address))

    def query_v6(self, address: ipaddress.IPv6Address) -> Point:
        return self._query(str(address))

    def _query(self, address: str) -> Point:
        result = self._reader.get_all(address)
        return Point(result.latitude, result.longitude)

    def _get_reader(self):
        reader = IP2LocationReader()
        reader.open(self._get_file('ip2location/IP2LOCATION-LITE-DB5.BIN'))
        return reader


interface = IP2Location
