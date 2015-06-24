"""
Tasks for the GeoIP databases app.
"""
import logging
from celery import task
from geodb import GeoDB


logger = logging.getLogger('tasks')


@task(bind=True, throws=(GeoDB.NotFoundError,))
def query_database(self, database_name, ip_address):
    """
    Queries a GeoIP database for a location for the given IP address.

    :param database_name: The name of the database to use.
    :type database_name: str
    :param ip_address: The IP address to get the location for.
    :type ip_address: str
    :return: The location of the IP address according to the database.
    :rtype: Point
    """
    try:
        interface = GeoDB.get_interface(database_name)
    except GeoDB.NotFoundError as e:
        logger.warn("No GeoDB interface for database with name '%s'." % database_name)
        raise e  # Re-raise exception, let Celery handle it further
    else:
        result = interface.query(ip_address)
        interface.close()

        if not result:
            logger.debug("No location obtained for address '%s' using database '%s'." % (ip_address, interface.codename))

        return result
