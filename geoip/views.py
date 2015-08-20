"""
General views for the GeoIP application.
"""
from django.views.generic import TemplateView
from geoip.measurements.models import Dataset, Measurement
from geoip.nodes.models import Node


class HomepageView(TemplateView):
    """
    Home page of the public site.
    """
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['statistics'] = self.get_statistics()
        return context

    def get_statistics(self):
        return {
            'node_count': Node.objects.active().usable().count(),
            'dataset_count': Dataset.objects.all().count(),
            'last_measurement': Measurement.objects.order_by('created').last(),
        }


class AboutView(TemplateView):
    """
    About page of the public site.
    """
    template_name = 'pages/about.html'
