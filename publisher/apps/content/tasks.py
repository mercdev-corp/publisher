from django.db.models import F

from publisher import celery_app

from .models import (
    Audio,
    Page,
    Text,
    Video
)


COUNTABLE = [
    Audio,
    Text,
    Video,
]


@celery_app.task
def count_view(pk):
    if not pk:
        return

    try:
        Page.objects.get(pk=pk)
    except (Page.DoesNotExist, ValueError):
        return

    for content in COUNTABLE:
        content.objects.filter(page_id=pk).update(counter=F('counter') + 1)
