from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'publisher.settings')

app = Celery('publisher')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
