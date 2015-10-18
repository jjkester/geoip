"""
Views for the GeoIP measurements app.
"""
from celery import chain
from django.core.cache import caches
from django.db.models import Count, Avg, Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.databases.models import Database
from geoip.measurements.models import Dataset, Measurement
from geoip.measurements.tasks import dataset_as_csv, set_cache


class DatasetListView(ListView):
    """
    Lists completed datasets.
    """
    queryset = Dataset.objects.public().completed().order_by('-end')\
        .annotate(nodes__count=Count('measurements__node', distinct=True))\
        .annotate(databases__count=Count('measurements__database', distinct=True))
    context_object_name = 'datasets'

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['measurements'] = Measurement.objects.filter(dataset__in=self.object_list)
        return context


class DatasetDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a completed dataset.
    """
    queryset = Dataset.objects.public().completed()\
        .annotate(nodes__count=Count('measurements__node', distinct=True))\
        .annotate(databases__count=Count('measurements__database', distinct=True))
    context_object_name = 'dataset'

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context['databases'] = Database.objects.filter(measurements__dataset=self.object).distinct()
        context['statistics'] = self.get_statistics()
        context['database_results'] = self.get_database_results()
        return context

    def get_statistics(self):
        aggregates = self.object.measurements.all()\
            .aggregate(
                accuracy_ipv4=Avg('ipv4_distance'),
                accuracy_ipv6=Avg('ipv6_distance'),
                accuracy_difference=Avg('mutual_distance'),
            )
        return aggregates

    def get_database_results(self):
        measurement_points = [1, 10, 25, 100, 250]
        query_v4 = lambda d, p:  self.object.measurements.exclude(ipv4_distance=None).filter(database=d, ipv4_distance__lte=p).count()
        query_v6 = lambda d, p:  self.object.measurements.exclude(ipv6_distance=None).filter(database=d, ipv6_distance__lte=p).count()
        databases = Database.objects.filter(measurements__dataset=self.object).distinct()

        averages = []
        ranges = []
        counts = []

        for database in databases:
            aggregates = self.object.measurements.filter(database=database).exclude(ipv4_distance=None)\
                .aggregate(
                    accuracy_ipv4=Avg('ipv4_distance'),
                    accuracy_ipv6=Avg('ipv6_distance'),
                    accuracy_difference=Avg('mutual_distance'),
                )
            averages.append(dict(
                database=database,
                **aggregates
            ))
            ranges.append({
                'database': database,
                'v4': {point: query_v4(database, point) for point in measurement_points},
                'v6': {point: query_v6(database, point) for point in measurement_points},
                'total': self.object.measurements.count(),
            })
            counts.append({
                'database': database,
                'all': self.object.measurements.filter(database=database).count(),
                'complete': self.object.measurements.filter(database=database).exclude(ipv4_location=None).exclude(ipv6_location=None).count(),
                'incomplete': self.object.measurements.filter(database=database).filter(Q(ipv4_location=None) | Q(ipv6_location=None)).count(),
                'only_v6': self.object.measurements.filter(database=database).exclude(ipv6_location=None).filter(ipv4_location=None).count(),
                'only_v4': self.object.measurements.filter(database=database).exclude(ipv4_location=None).filter(ipv6_location=None).count(),
            })

        return {
            'averages': averages,
            'ranges': ranges,
            'counts': counts,
        }


class MeasurementDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a measurement.
    """
    queryset = Measurement.objects.filter(dataset__in=Dataset.objects.public().completed())
    context_object_name = 'measurement'


class DatasetExportView(HashidsSingleObjectMixin, DetailView):
    """
    Exports a dataset as CSV file.
    """
    queryset = Dataset.objects.public().completed()
    template_name_suffix = '_export'
    context_object_name = 'dataset'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        cache_name = 'filesystem'
        cache_key = 'dataset_%s_csv' % self.object.hashid

        cache = caches[cache_name]

        content = cache.get(cache_key)

        if content is None or content is False:
            if content is None:
                cache.set(cache_key, False, None)
                prepare_csv_export = chain(
                    dataset_as_csv.s(self.object.pk),
                    set_cache.s(cache_name=cache_name, key=cache_key, timeout=86400)
                )
                prepare_csv_export()
            response = super(DatasetExportView, self).get(request, *args, **kwargs)
        else:
            response = HttpResponse(content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.object.hashid

        return response
