"""
Contains a management command for scraping sources for new nodes.
"""
from django.core.management import CommandError
from django.core.management.base import LabelCommand


class Command(LabelCommand):
    """
    Management command for scraping sources for new nodes.
    """
    help = "Scrapes sources for new nodes"

    def handle_label(self, label, **options):
        try:
            module = __import__('geoip.scrapers.%s' % label, fromlist=['geoip.scrapers'])
            scraper = module.Scraper()
        except (ImportError, AttributeError):
            raise CommandError("Scraper %s does not exist" % label)

        scraper.initialize(**options)

        self.stdout.write("Scraping %s, this can take a while..." % label)

        count = scraper.handle()

        self.stdout.write("Scraped %d objects resulting in %d new nodes." % count)
