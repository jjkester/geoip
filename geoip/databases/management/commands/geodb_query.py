"""
Contains a management command for querying GeoDB database interfaces.
"""
from django.core.management import BaseCommand, CommandError
from geodb import GeoDB


class Command(BaseCommand):
    """
    Management command for querying GeoDB database interfaces.
    """
    help = "Query a GeoDB database interfaces"

    def add_arguments(self, parser):
        parser.add_argument('interface', nargs=1)
        parser.add_argument('ip_addresses', metavar='ip_addresses', nargs='+')

    def handle(self, interface, ip_addresses, **options):
        try:
            interface = GeoDB.get_interface(interface[0])
        except GeoDB.NotFoundError as e:
            raise CommandError(e)

        for ip_address in ip_addresses:
            result = interface.query(ip_address)
            location = "%f, %f" % (result[0], result[1]) if result else "(unknown)"
            self.stdout.write("Location for %s:\n    %s" % (ip_address, location))

        interface.close()
