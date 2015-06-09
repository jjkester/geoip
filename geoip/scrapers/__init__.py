class BaseScraper(object):
    """
    Base class for scrapers.
    """
    def initialize(self, **kwargs):
        """
        Allows the scraper to set settings or prepare for scraping. Is called before handle.
        """
        pass

    def handle(self):
        """
        Should handle the scraping process.
        """
        pass
