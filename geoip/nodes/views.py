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
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(NodeListView, self).get_context_data(**kwargs)
        context['all_nodes'] = Node.objects.all()
        context['page_numbers'] = [1, context['paginator'].num_pages]
        context['page_numbers'].extend([n for n in context['paginator'].page_range if abs(context['page_obj'].number - n) < 5])
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


class NodeMapView(ListView):
    """
    Displays nodes on a map.
    """
    template_name_suffix = '_map'
    context_object_name = 'nodes'
    queryset = Node.objects.active().usable()

    def get_context_data(self, **kwargs):
        context = super(NodeMapView, self).get_context_data(**kwargs)
        context['points'] = self.object_list.values_list('location', flat=True)
        return context
