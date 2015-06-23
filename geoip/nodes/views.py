"""
Views for the GeoIP nodes app.
"""
from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.measurements.models import Dataset
from geoip.nodes.models import Node, DataSource


class NodeView(TemplateView):
    """
    Section overview page.
    """
    template_name = 'nodes/index.html'

    def get_context_data(self, **kwargs):
        context = super(NodeView, self).get_context_data(**kwargs)
        context['sources'] = DataSource.objects.all().annotate(nodes__count=Count('nodes')).order_by('-nodes__count')
        context['nodes'] = Node.objects.all()
        return context


class NodeListView(ListView):
    """
    Lists active nodes.
    """
    queryset = Node.objects.active().usable()
    context_object_name = 'nodes'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(NodeListView, self).get_context_data(**kwargs)
        context['all_nodes'] = Node.objects.all()
        return context


class NodeDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows an active node.
    """
    queryset = Node.objects.active().usable()
    context_object_name = 'node'

    def get_context_data(self, **kwargs):
        context = super(NodeDetailView, self).get_context_data(**kwargs)
        context['datasets'] = Dataset.objects.filter(
            measurements__in=self.object.measurements.all()).distinct().order_by('-start')[:10]
        return context
