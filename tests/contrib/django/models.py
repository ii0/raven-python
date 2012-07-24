from __future__ import absolute_import

from django.db import models
from sentry.models import GzippedDictField


class TestModel(models.Model):
    data = GzippedDictField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.data)
