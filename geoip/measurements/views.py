"""
Views for the GeoIP measurements app.
"""
from django.db.models import Count, F, Avg
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.databases.models import Database
from geoip.measurements.models import Dataset, Measurement


class DatasetListView(ListView):
    """
    Lists completed datasets.
    """
    queryset = Dataset.objects.public().completed()\
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

        return {
            'averages': averages,
            'ranges': ranges,
        }


class MeasurementDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a measurement.
    """
    queryset = Measurement.objects.filter(dataset__in=Dataset.objects.public().completed())
    context_object_name = 'measurement'
