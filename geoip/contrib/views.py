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
            decoded = self.queryset.model.hashids.decode(self.kwargs.get('hashid'))
            if decoded and len(decoded) == 1:
                self.kwargs['pk'] = decoded[0]
            else:
                self.kwargs['pk'] = -1
        return super(HashidsSingleObjectMixin, self).get_object(queryset)
