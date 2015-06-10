"""
Contains a management command for setting up GeoDB database interfaces.
"""
from django.core.management import CommandError
from django.core.management.base import LabelCommand
from geodb import GeoDB
from geoip.databases.models import Database


class Command(LabelCommand):
    """
    Management command for setting up GeoDB database interfaces.
    """
    help = "Perform initial setup steps for GeoDB database interfaces"

    def handle_label(self, label, **options):
        try:
            interface = GeoDB.get_interface(label)
        except GeoDB.NotFoundError as e:
            raise CommandError(e)

        obj, created = Database.objects.update_or_create(
            codename=interface.codename,
            defaults=dict(
                name=interface.name,
                version=interface.get_version(),
                url=interface.url,
                notes=interface.license,
            ),
        )

        self.stdout.write("Initialized %s:" % label)
        self.stdout.write("  - Name: {name:s}\n  - Current version: {version:s}".format(name=obj.name,
                                                                                        version=obj.version))

        interface.close()
