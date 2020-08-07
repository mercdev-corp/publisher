from django.db.transaction import on_commit
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from publisher.apps.content.models import Page
from publisher.apps.content.tasks import count_view

from .serializers import (
    PageListSerializer,
    PageSerializer
)


class PageListAPIView(ListAPIView):
    serializer_class = PageListSerializer
    queryset = Page.objects.all()


class PageRetrieveAPIView(RetrieveAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()  # `prefetch_related` not used here
                                   # because resulted number of DB requestes will stay same
                                   # but will consume more resources because
                                   # will try to prefetch all records

    def retrieve(self, request, *args, **kwargs):
        result = super().retrieve(request, *args, **kwargs)

        on_commit(lambda: count_view.delay(pk=kwargs['pk']))

        return result
