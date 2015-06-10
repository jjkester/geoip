"""
Interfaces for GeoIP databases.
"""


class GeoDB(object):
    """
    Helper class for working with GeoDB.
    """
    class NotFoundError(Exception):
        pass

    @staticmethod
    def get_interface(name):
        try:
            module = __import__('geodb.%s' % name, fromlist=['geodb'])
            return module.interface()
        except (ImportError, AttributeError):
            raise GeoDB.NotFoundError("Database interface %s does not exist" % name)
