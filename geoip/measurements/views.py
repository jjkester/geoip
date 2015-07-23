"""
Views for the GeoIP measurements app.
"""
from django.db.models import Count
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.measurements.models import Dataset, Measurement


class DatasetListView(ListView):
    """
    Lists completed datasets.
    """
    queryset = Dataset.objects.filter(status=int(Dataset.Status.success), is_public=True).annotate(
        nodes__count=Count('measurements__node')).annotate(databases__count=Count('measurements__database'))
    context_object_name = 'datasets'

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['measurements'] = Measurement.objects.filter(dataset__in=self.object_list)
        return context


class DatasetDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a completed dataset.
    """
    queryset = Dataset.objects.filter(status=int(Dataset.Status.success), is_public=True).annotate(
        nodes__count=Count('measurements__node')).annotate(databases__count=Count('measurements__database'))
    context_object_name = 'dataset'


class MeasurementDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a measurement.
    """
    queryset = Measurement.objects.filter(dataset__status=int(Dataset.Status.success), dataset__is_public=True)
    context_object_name = 'measurement'