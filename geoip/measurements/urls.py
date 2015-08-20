"""
URLs for the GeoIP measurements app.
"""
from django.conf.urls import url
from geoip.measurements.views import DatasetListView, DatasetDetailView, MeasurementDetailView, DatasetExportView

urlpatterns = [
    url(r'^datasets/list/$', DatasetListView.as_view(), name='dataset_list'),
    url(r'^datasets/list/(?P<page>\d+)/$', DatasetListView.as_view(), name='dataset_list'),
    url(r'^datasets/show/(?P<hashid>\w+)/$', DatasetDetailView.as_view(), name='dataset_detail'),
    url(r'^datasets/export/(?P<hashid>\w+)/$', DatasetExportView.as_view(), name='dataset_export'),
    url(r'^show/(?P<hashid>\w+)/$', MeasurementDetailView.as_view(), name='measurement_detail'),
]
