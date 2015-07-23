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


def get_pagination_range(page_obj, count=15):
    count = int(count / 2)
    first = 1
    current = page_obj.number
    last = page_obj.paginator.num_pages
    before = min(current - first, count)
    after = min(last - current, count)

    if before < count:
        after = min(last - current - 1, after + count - before)
    if after < count:
        before = min(current - 1, before + count - after)

    print("Cnt=%d Cur=%d Lst=%d Bef=%d Aft=%d" % (count, current, last, before, after))

    return range(current - before, current + after + 1)
