import os, sys

from split_settings.tools import optional, include


include(
    'main.py',
    'apps.py',
    'celery.py',
    'rest.py',
    'connections.py',
    'accounts.py',

    scope=locals()
)

if os.environ.get('DOCKER_CONTAINER'):
    include(
        'docker.py',
        optional('../docker_settings_local.py'),

        scope=locals()
    )

if os.environ.get('DJANGO_TESTING') or 'test' in sys.argv or'test_coverage' in sys.argv:
    include(
        optional('test.py'),

        scope=locals()
    )

if not os.environ.get('DOCKER_CONTAINER'):
    include(
        optional('../settings_local.py'),

        scope=locals()
    )
