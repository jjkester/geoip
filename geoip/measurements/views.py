"""
Views for the GeoIP measurements app.
"""
import csv
from django.db.models import Count, Avg, Q
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.databases.models import Database
from geoip.measurements.models import Dataset, Measurement


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


class DatasetExportView(HashidsSingleObjectMixin, SingleObjectMixin, View):
    """
    Exports a dataset as CSV file.
    """
    queryset = Dataset.objects.public().completed().prefetch_related('measurements', 'measurements__node')

    def get_csv_data(self):
        def format_location(point):
            if point:
                return point.x, point.y
            return None

        data = []

        data.append((
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

        for measurement in self.object.measurements.all():
            data.append((
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

        return data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % self.object.hashid

        writer = csv.writer(response)

        for row in self.get_csv_data():
            writer.writerow(row)

        return response
