"""
General views for the GeoIP application.
"""
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    """
    Home page of the public site.
    """
    template_name = 'pages/index.html'
