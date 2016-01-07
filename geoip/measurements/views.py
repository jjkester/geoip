"""
Views for the GeoIP measurements app.
"""
from celery import chain
from django.core.cache import caches
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.measurements.analysis import DataSetAnalysis
from geoip.measurements.models import Dataset, Measurement
from geoip.measurements.tasks import dataset_as_csv, set_cache, dataset_accuracy_as_csv


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

        analysis = DataSetAnalysis(self.object)

        context['databases'] = analysis.databases
        context['statistics'] = analysis.averages()
        context['database_results'] = {
            'accuracies': analysis.database_accuracies([1, 10, 25, 50, 100, 250, 500, 1000]),
            'averages': analysis.database_averages(),
            'counts': analysis.database_counts(),
        }

        return context


class DatasetChartView(HashidsSingleObjectMixin, DetailView):
    """
    Shows a single SVG chart.
    """
    queryset = Dataset.objects.public().completed()
    content_type = 'image/svg+xml'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        analysis = DataSetAnalysis(self.object)
        try:
            chart_method = '%s_chart' % self.kwargs['method']
            content = getattr(analysis, chart_method)(for_embed=False)
        except AttributeError:
            raise Http404("No chart named %s." % chart_method)
        return HttpResponse(
                content=content,
                content_type=self.content_type,
            )


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
    task = dataset_as_csv
    filename_suffix = ''

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        cache_name = 'filesystem'
        cache_key = 'dataset_%s%s_csv' % (self.object.hashid, self.filename_suffix)

        cache = caches[cache_name]

        content = cache.get(cache_key)

        if content is None or content is False:
            if content is None:
                cache.set(cache_key, False, None)
                prepare_csv_export = chain(
                    self.task.s(self.object.pk),
                    set_cache.s(cache_name=cache_name, key=cache_key, timeout=86400)
                )
                prepare_csv_export()
            response = super(DatasetExportView, self).get(request, *args, **kwargs)
        else:
            response = HttpResponse(content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s%s.csv"' % (self.object.hashid, self.filename_suffix)

        return response


class DatasetAccuracyExportView(DatasetExportView):
    """
    Exports the accuracy results of a dataset as CSV file.
    """
    filename_suffix = '_accuracy'
    task = dataset_accuracy_as_csv
