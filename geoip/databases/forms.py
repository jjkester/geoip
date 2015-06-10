"""
Forms for the GeoIP databases app.
"""
from django import forms
from django.utils.translation import ugettext_lazy as _


class IPAddressForm(forms.Form):
    """
    Form for entering a single IP address.
    """
    ip_address = forms.GenericIPAddressField(
        label=_("IP address"),
        error_messages={
            'required': _("Please enter an IP address."),
            'invalid': _("The entered IP address is not a valid IPv4 or IPv6 address."),
        }
    )
