"""
Contains a management command for getting information on GeoDB database interfaces.
"""
from django.core.management import CommandError
from django.core.management.base import LabelCommand
from geodb import GeoDB


class Command(LabelCommand):
    """
    Management command for getting information on GeoDB database interfaces.
    """
    help = "Get information for GeoDB database interfaces"

    def handle_label(self, label, **options):
        try:
            interface = GeoDB.get_interface(label)
        except GeoDB.NotFoundError as e:
            raise CommandError(e)

        self.stdout.write("Interface %s:" % label)
        self.stdout.write("  - Name:             {name:s}\n"
                          "  - Current version:  {version:s}\n"
                          "  - URL:              {url:s}\n"
                          "  - License:          {license:s}".format(name=interface.name,
                                                                     version=interface.get_version(),
                                                                     url=interface.url,
                                                                     license=interface.license))

        interface.close()
