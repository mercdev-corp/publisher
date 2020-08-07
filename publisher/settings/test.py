CELERY_TASK_ALWAYS_EAGER = True
CELERY_BEAT_SCHEDULE = {}
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 1
}
