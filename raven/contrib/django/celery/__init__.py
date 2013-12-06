"""
raven.contrib.django.celery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from raven.contrib.celery import CeleryMixin
from raven.contrib.django.client import DjangoClient
try:
    from celery.contrib.methods import task
except ImportError:
    # Import the pre Celery 3.1 tasks (At some point we'll drop that)
    try:
        from celery.task import task
    except ImportError:
        from celery.decorators import task  # NOQA


class CeleryClient(CeleryMixin, DjangoClient):

    def send_integrated(self, kwargs):
        return send_raw_integrated.delay(kwargs)

    def send_encoded(self, *args, **kwargs):
        "Errors through celery"
        return send_raw.delay(*args, **kwargs)


@task(routing_key='sentry')
def send_raw_integrated(kwargs):
    from raven.contrib.django.models import get_client
    super(DjangoClient, get_client()).send_integrated(kwargs)


@task(routing_key='sentry')
def send_raw(*args, **kwargs):
    from raven.contrib.django.models import get_client
    super(DjangoClient, get_client()).send_encoded(*args, **kwargs)
