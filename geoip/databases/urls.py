"""
URLs for the GeoIP databases app.
"""
from django.conf.urls import url
from geoip.databases.views import DatabaseListView, DatabaseDetailView, DatabaseQueryResultView, DatabaseQueryFormView

urlpatterns = [
    url(r'^list/$', DatabaseListView.as_view(), name='database_list'),
    url(r'^list/(?P<page>\d+)/$', DatabaseListView.as_view(), name='database_list'),
    url(r'^show/(?P<hashid>\w+)/$', DatabaseDetailView.as_view(), name='database_detail'),
    url(r'^query/(?P<hashid>\w+)/$', DatabaseQueryFormView.as_view(), name='database_query'),
    url(r'^query/(?P<hashid>\w+)/(?P<ip_address>[0-9a-fA-F:\.]+)/$', DatabaseQueryResultView.as_view(), name='database_query'),
]
