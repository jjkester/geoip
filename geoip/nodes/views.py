"""
Views for the GeoIP nodes app.
"""
from django.views.generic import TemplateView, ListView, DetailView
from geoip.contrib.views import HashidsSingleObjectMixin
from geoip.nodes.models import Node, DataSource


class NodeView(TemplateView):
    """
    Section overview page.
    """
    template_name = 'nodes/index.html'

    def get_context_data(self, **kwargs):
        context = super(NodeView, self).get_context_data(**kwargs)
        context['sources'] = DataSource.objects.all()
        context['nodes'] = Node.objects
        return context


class NodeListView(ListView):
    """
    Lists active nodes.
    """
    queryset = Node.objects.useable()
    context_object_name = 'nodes'
    paginate_by = 20


class NodeDetailView(HashidsSingleObjectMixin, DetailView):
    """
    Shows an active node.
    """
    queryset = Node.objects.useable()
    context_object_name = 'node'
