import itertools
from celery import chain
from django.utils.translation import ugettext_lazy as _
from geoip.databases.models import Database
from geoip.measurements.tasks import perform_measurement, dataset_pre_measurement, dataset_post_measurement
from geoip.nodes.models import Node


def run_measurements(modeladmin, request, queryset):
    # Prepare measurement job arguments
    databases = Database.objects.active().values_list('id', flat=True)
    nodes = Node.objects.active().usable().values_list('id', flat=True)

    for dataset in queryset:
        dataset_pre_measurement(dataset.pk)
        # Dispatch measurement jobs in groups of 10
        jobs = perform_measurement.chunks(itertools.product([dataset.pk], databases, nodes), 10)
        chain(jobs, dataset_post_measurement.s(dataset_id=dataset.pk)).apply_async()
run_measurements.short_description = _("Run measurements for selected datasets")
