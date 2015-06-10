"""
URLs for the GeoIP databases app.
"""
from django.conf.urls import url
from geoip.databases.views import DatabaseListView, DatabaseDetailView

urlpatterns = [
    url(r'^list/$', DatabaseListView.as_view(), name='database_list'),
    url(r'^list/(?P<page>\d+)/$', DatabaseListView.as_view(), name='database_list'),
    url(r'^show/(?P<hashid>\w+)/$', DatabaseDetailView.as_view(), name='database_detail'),
]
