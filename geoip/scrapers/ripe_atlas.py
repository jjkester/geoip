from django.contrib.gis.geos import Point
from django.db import transaction
import requests
from geoip.nodes.models import Node, DataSource
from geoip.scrapers import BaseScraper


class Scraper(BaseScraper):
    """
    Retrieves all RIPE Atlas probes and adds them as Nodes to the application.
    """
    def handle(self):
        source, created = DataSource.objects.get_or_create(name="RIPE Atlas", url="https://atlas.ripe.net/")
        counter_total = 0
        counter_created = 0
        url = "/api/v1/probe/"

        try:
            while url is not None:
                response = requests.get("https://atlas.ripe.net%s" % url, params={'limit': 100})
                data = response.json()

                with transaction.atomic():
                    for probe in data['objects']:
                        if probe['latitude'] and probe['longitude']:
                            point = Point(probe['latitude'], probe['longitude'], srid=4326)
                        else:
                            point = None

                        obj, created = Node.objects.update_or_create(
                            name="RIPE Atlas #{id:d}".format(id=probe['id']),
                            source=source,
                            defaults=dict(
                                location=point,
                                ipv4=probe['address_v4'],
                                ipv6=probe['address_v6'],
                            )
                        )

                        if created:
                            counter_created += 1
                        counter_total += 1

                url = data['meta']['next']
        except KeyboardInterrupt:
            print("Process interrupted by user.")
        return counter_total, counter_created
