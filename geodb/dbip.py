"""
Interface for the DB-IP "IP Address Location" database.

URL: https://db-ip.com/db/

Requires the database (in CSV format) to be locally available.
"""
import csv
import ipaddress
import os
import sqlite3
from django.contrib.gis.geos import Point
from django.utils.datetime_safe import datetime
from geodb.interfaces import GeoIPInterface


class DBIP(GeoIPInterface):
    """
    Interface for the DB-IP "IP Address Location" database.

    Automatically builds an SQLite3 database from the CSV database to enhance performance.
    """
    name = "DB-IP IP address to location"
    codename = "dbip"
    url = "https://db-ip.com/db/"
    license = "Database provided by DB-IP for research purposes only."

    def __init__(self):
        super().__init__()
        self._conn = self._get_conn()

    def close(self):
        self._conn.close()

    def get_version(self):
        return datetime.fromtimestamp(os.path.getmtime(self._get_file('db-ip/dbip-location.csv'))).strftime('%Y-%m-%d')

    def query_v4(self, address: ipaddress.IPv4Address) -> Point:
        return self._query(str(address))

    def query_v6(self, address: ipaddress.IPv6Address) -> Point:
        return self._query(str(address))

    def _query(self, address: str) -> Point:
        cursor = self._conn.cursor()
        result = cursor.execute(
            "SELECT latitude, longitude FROM location WHERE ip_start >= ? AND ip_end <= ?;",
            (address, address)
        ).fetchone()

        if result:
            return Point(
                result[0],
                result[1],
                srid=4326,
            )
        return None

    def _get_conn(self):
        path = self._get_file('db-ip/dbip-location.db')

        if not os.path.exists(path):
            # SQLite3 database does not exist, build from csv
            open(path, 'a').close()

            conn = sqlite3.connect(path)
            cursor = conn.cursor()

            # Create table
            cursor.execute("CREATE TABLE location ("
                           "ip_start TEXT PRIMARY KEY NOT NULL,"
                           "ip_end TEXT NOT NULL,"
                           "country TEXT NOT NULL,"
                           "stateprov TEXT NOT NULL,"
                           "city TEXT NOT NULL,"
                           "latitude REAL NOT NULL,"
                           "longitude REAL NOT NULL,"
                           "timezone_offset REAL NOT NULL,"
                           "timezone_name TEXT NOT NULL);")
            conn.commit()

            # Import csv
            with open(self._get_file('db-ip/dbip-location.csv'), 'r') as source:
                reader = csv.reader(source, delimiter=',', quotechar='"')
                cursor.executemany(
                    "INSERT INTO location (ip_start, ip_end, country, stateprov, city, latitude, longitude,"
                    "timezone_offset, timezone_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
                    [(x + ([None] * (9 - len(x))))[:9] for x in reader]
                )
                conn.commit()
                conn.close()

        return sqlite3.connect(path)

interface = DBIP
