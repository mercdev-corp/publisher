#!/usr/bin/env bash

set -e
set -x

export DEBIAN_FRONTEND=noninteractive

ROOT=/publisher
ENV=$ROOT/env
PY=$ENV/bin/python
PROJ=$ROOT/publisher
MANAGE=$PROJ/manage.py

if [ ! -d "$ENV/bin" ] ; then
    mkdir -p $ROOT
    chmod -R a+rwx $ROOT
    pip install virtualenv
    virtualenv -p python3.8 $ENV
    $ENV/bin/pip install -U pip setuptools
fi

cd $PROJ

$ENV/bin/pip install -r requirements.txt
chmod a+rwx $ROOT/media
mkdir -p $ROOT/media/static
mkdir -p $ROOT/media/uploads
chmod a+rwx $ROOT/media/static
chmod a+rwx $ROOT/media/uploads

case "$1" in
    runserver)
        $PY $MANAGE migrate
        $PY $MANAGE runserver 0.0.0.0:8000
    ;;

    test)
        $PY $MANAGE test --noinput
    ;;

    celery)
        $PY -m celery -A publisher worker -B -l debug
    ;;

    *)
        $PY $MANAGE migrate
        $PY $MANAGE collectstatic --noinput
        $ENV/bin/daphne -b 0.0.0.0 -p 8080 publisher.asgi:application
    ;;
esac
