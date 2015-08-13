"""
Tasks for the GeoIP measurements app.
"""
import logging
from celery import task
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from geoip.databases.models import Database
from geoip.databases.tasks import query_database
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
