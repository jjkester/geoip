"""
View mixins for the GeoIP application.
"""


class HashidsSingleObjectMixin(object):
    """
    View mixin that provides object lookup through a hash ID.

    Requires the model to have an attribute ``hashids`` containing a ``Hashids`` instance.
    """
    def get_object(self, queryset=None):
        if 'hashid' in self.kwargs and not 'pk' in self.kwargs:
            self.kwargs['pk'] = self.queryset.model.hashids.decode(self.kwargs.get('hashid'))[0]
        return super(HashidsSingleObjectMixin, self).get_object(queryset)
