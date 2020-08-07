from django.urls import path

from .views import (
    PageListAPIView,
    PageRetrieveAPIView
)


urlpatterns = [
    path('page/list/', PageListAPIView.as_view(),
         name='content_page_v1_list'),
    path('page/<int:pk>/', PageRetrieveAPIView.as_view(),
         name='content_page_v1_detail'),
]
