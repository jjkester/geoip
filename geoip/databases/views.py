"""
Views for the GeoIP databases app.
"""
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from geodb import GeoDB
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.databases.forms import IPAddressForm
from geoip.databases.models import Database
from geoip.measurements.models import Dataset


class DatabaseListView(ListView):
    """
    Lists active databases.
    """
    queryset = Database.objects.active()
    context_object_name = 'databases'


class DatabaseDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows an active database.
    """
    queryset = Database.objects.all()
    context_object_name = 'database'

    def get_context_data(self, **kwargs):
        context = super(DatabaseDetailView, self).get_context_data(**kwargs)
        context['datasets'] = Dataset.objects.public().completed().filter(measurements__database=self.object)
        return context


class DatabaseQueryResultView(HashidsSingleObjectMixin, DetailView):
    """
    Shows the query result for an active database.
    """
    queryset = Database.objects.active()
    template_name_suffix = '_query'
    context_object_name = 'database'
    form_class = IPAddressForm

    def get_context_data(self, **kwargs):
        context = super(DatabaseQueryResultView, self).get_context_data(**kwargs)
        context['ip_address'] = self.kwargs['ip_address']
        context['location'] = self.get_location()
        context['form'] = self.form_class(initial={'ip_address': self.kwargs['ip_address']})
        return context

    def get_location(self):
        ip_address = self.kwargs['ip_address']
        interface = GeoDB.get_interface(self.object.codename)
        location = interface.query(ip_address)
        interface.close()
        return location


class DatabaseQueryFormView(HashidsSingleObjectMixin, UpdateView):
    """
    Shows the form to query an active database
    """
    queryset = Database.objects.active()
    template_name_suffix = '_query'
    context_object_name = 'database'
    form_class = IPAddressForm

    def get_form_kwargs(self):
        kwargs = super(DatabaseQueryFormView, self).get_form_kwargs()
        del kwargs['instance']
        return kwargs

    def form_valid(self, form):
        return HttpResponseRedirect(reverse_lazy('databases:database_query', kwargs={'hashid': self.object.hashid,
                                                                                     'ip_address': form.cleaned_data[
                                                                                         'ip_address']}))
