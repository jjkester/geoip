import os
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv6_address, validate_ipv4_address
from django.db import transaction
from geoip.nodes.models import Node, DataSource
from geoip.scrapers import BaseScraper


class Scraper(BaseScraper):
    """
    Reads a text file and adds the contents as Caida Ark nodes.

    The file should consist of lines of the following format:

        <name> <ipv4> <ipv6> <lat> <lon> <location_name>

    The text file should be called `caida.txt` and be located in the `databases` folder.
    """
    def handle(self):
        source, created = DataSource.objects.get_or_create(name="CAIDA Archipelago (Ark)",
                                                           url="http://www.caida.org/projects/ark/")
        counter_total = 0
        counter_created = 0

        path = os.path.join(settings.BASE_DIR, 'databases', 'caida.txt')
        file = open(path)

        try:
            for line in file:
                try:
                    name, ipv4, ipv6, lat, lon, location = line.split(' ', 5)
                except ValueError:
                    continue

                # Create point
                try:
                    point = Point(float(lat), float(lon), srid=4326)
                except TypeError:
                    point = None

                # Test for unset IP addresses
                try:
                    validate_ipv4_address(ipv4)
                except ValidationError:
                    ipv4 = None
                try:
                    validate_ipv6_address(ipv6)
                except ValidationError:
                    ipv6 = None

                with transaction.atomic():
                    obj, created = Node.objects.update_or_create(
                        name="CAIDA Ark {name:s}".format(name=name),
                        source=source,
                        defaults=dict(
                            location=point,
                            ipv4=ipv4,
                            ipv6=ipv6,
                        )
                    )

                    if created:
                        counter_created += 1
                    counter_total += 1
        except KeyboardInterrupt:
            print("Process interrupted by user.")
        return counter_total, counter_created
