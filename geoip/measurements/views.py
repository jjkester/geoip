"""
Views for the GeoIP measurements app.
"""
from django.db.models import Count, F, Avg
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
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
        context['statistics'] = self.get_statistics()
        return context

    def get_statistics(self):
        aggregates = self.object.measurements.exclude(ipv4_distance=None)\
            .aggregate(
                accuracy_ipv4=Avg('ipv4_distance'),
                accuracy_ipv6=Avg('ipv6_distance'),
                accuracy_difference=Avg('mutual_distance'),
            )
        return aggregates


class MeasurementDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a measurement.
    """
    queryset = Measurement.objects.filter(dataset__in=Dataset.objects.public().completed())
    context_object_name = 'measurement'
