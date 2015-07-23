"""
URLs for the GeoIP nodes app.
"""
from django.conf.urls import url
from geoip.nodes.views import NodeListView, NodeDetailView, NodeView, NodeMapView

urlpatterns = [
    url(r'^$', NodeView.as_view(), name='index'),
    url(r'^list/$', NodeListView.as_view(), name='node_list'),
    url(r'^list/(?P<page>\d+)/$', NodeListView.as_view(), name='node_list'),
    url(r'^show/(?P<hashid>\w+)/$', NodeDetailView.as_view(), name='node_detail'),
    url(r'^map/$', NodeMapView.as_view(), name='node_map'),
]
