from django.urls import include, path

from .apps.content.api.v1 import urls as content_v1_urls


urlpatterns = [
    path('v1/', include(content_v1_urls)),
]
