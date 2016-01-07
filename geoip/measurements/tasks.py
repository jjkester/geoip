"""
Tasks for the GeoIP measurements app.
"""
import csv
import io
import logging
from celery import task
from django.core.cache import caches
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from geoip.databases.models import Database
from geoip.databases.tasks import query_database
from geoip.measurements.analysis import DataSetAnalysis
from geoip.measurements.models import Dataset, Measurement
from geoip.nodes.models import Node


logger = logging.getLogger('tasks')


@task(throws=(ObjectDoesNotExist,))
def perform_measurement(dataset_id, database_id, node_id):
    """
    Performs a measurement on the given node using the given database. A new :py:class:`Measurement` object will be
    created within the given dataset. In case a measurement for this database and node already exists in the database
    the old result will be overwritten.

    :param dataset_id: The id of the dataset the measurement is for.
    :param database_id: The id of the database to use for queries.
    :param node_id: The id of the node to investigate.
    :return: The id of the measurement.
    """
    dataset = Dataset.objects.get(pk=dataset_id)
    database = Database.objects.get(pk=database_id)
    node = Node.objects.get(pk=node_id)

    ipv4_location = query_database(database.codename, node.ipv4) if node.ipv4 else None
    ipv6_location = query_database(database.codename, node.ipv6) if node.ipv6 else None

    measurement, created = Measurement.objects.update_or_create(
        dataset=dataset,
        database=database,
        node=node,
        defaults=dict(
            ipv4_location=ipv4_location,
            ipv6_location=ipv6_location,
        )
    )
    measurement.calculate_distances()
    measurement.save()

    return measurement.pk


@task(throws=(ObjectDoesNotExist,))
def calculate_measurement_distances(measurement_id):
    measurement = Measurement.objects.get(pk=measurement_id)
    with transaction.atomic():
        measurement.calculate_distances()
        measurement.save()
    return measurement.pk


@task(throws=(ObjectDoesNotExist,))
def dataset_pre_measurement(dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.start = timezone.now()
    dataset.status = Dataset.Status.running
    dataset.save()
    return dataset.pk


@task(throws=(ObjectDoesNotExist,))
def dataset_post_measurement(result, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.status = Dataset.Status.success
    dataset.end = timezone.now()
    dataset.save()
    return dataset.pk


@task()
def dataset_as_csv(dataset_id):
    dataset = Dataset.objects.prefetch_related('measurements', 'measurements__node').get(pk=dataset_id)

    def format_location(point):
        if point:
            return point.x, point.y
        return None

    csv_data = []

    csv_data.append((
        "ID",
        "Database ID",
        "Node ID",
        "IPv4 address",
        "IPv6 address",
        "Location",
        "IPv4 location",
        "IPv6 location",
        "IPv4 distance",
        "IPv6 distance",
        "Mutual distance",
    ))

    for measurement in dataset.measurements.all():
        csv_data.append((
            measurement.hashid,
            measurement.database.hashid,
            measurement.node.hashid,
            measurement.node.ipv4 or '',
            measurement.node.ipv6 or '',
            format_location(measurement.node.location) or '',
            format_location(measurement.ipv4_location) or '',
            format_location(measurement.ipv6_location) or '',
            measurement.ipv4_distance or '',
            measurement.ipv6_distance or '',
            measurement.mutual_distance or '',
        ))

    output = io.StringIO()
    writer = csv.writer(output)

    for row in csv_data:
        writer.writerow(row)

    return output.getvalue()


@task()
def dataset_accuracy_as_csv(dataset_id, distance_step=5):
    dataset = Dataset.objects.prefetch_related('measurements').get(pk=dataset_id)

    points = range(0, 20001, distance_step)

    analysis = DataSetAnalysis(dataset)
    analysis_data = analysis.database_accuracies(points)

    csv_data = []
    csv_header_row = [""]

    column_data = []

    for analysis_row in analysis_data:
        csv_header_row.append(analysis_row['database'].name + (" (IPv4)"))
        csv_header_row.append(analysis_row['database'].name + (" (IPv6)"))

        column_data.append(list(map(lambda x: (x / analysis_row['total_v4']) * 100, analysis_row['ipv4'])))
        column_data.append(list(map(lambda x: (x / analysis_row['total_v6']) * 100, analysis_row['ipv6'])))

    csv_data.append(csv_header_row)

    for p in range(0, len(points)):
        csv_row = [points[p]]
        for col in column_data:
            csv_row.append(col[p])
        csv_data.append(csv_row)

    output = io.StringIO()
    writer = csv.writer(output)

    for row in csv_data:
        writer.writerow(row)

    return output.getvalue()


@task()
def set_cache(data, cache_name, key, timeout=-1):
    cache = caches[cache_name]
    if timeout >= 0:
        cache.set(key, data, timeout)
    else:
        cache.set(key, data)
