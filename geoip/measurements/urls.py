"""
URLs for the GeoIP measurements app.
"""
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from geoip.measurements.views import DatasetListView, DatasetDetailView, MeasurementDetailView, DatasetExportView, \
    DatasetChartView, DatasetAccuracyExportView

urlpatterns = [
    url(r'^datasets/list/$', DatasetListView.as_view(), name='dataset_list'),
    url(r'^datasets/list/(?P<page>\d+)/$', DatasetListView.as_view(), name='dataset_list'),
    url(r'^datasets/show/(?P<hashid>\w+)/$', DatasetDetailView.as_view(), name='dataset_detail'),
    url(r'^datasets/show/(?P<hashid>\w+)/chart/(?P<method>\w+)\.svg$', cache_page(86400, cache='filesystem')(DatasetChartView.as_view()), name='dataset_chart'),
    url(r'^datasets/export/(?P<hashid>\w+)/$', DatasetExportView.as_view(), name='dataset_export'),
    url(r'^datasets/export/(?P<hashid>\w+)/accuracy/$', DatasetAccuracyExportView.as_view(), name='dataset_export_accuracy'),
    url(r'^show/(?P<hashid>\w+)/$', MeasurementDetailView.as_view(), name='measurement_detail'),
]
