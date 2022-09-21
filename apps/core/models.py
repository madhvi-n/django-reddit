from django.db import models
import datetime


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updated ``created_at``
    and ``updated_at`` fields
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    visitable = False

    class Meta:
        abstract = True

    def is_edited(self):
        return (self.updated_at - self.created_at).total_seconds() > 1
    edited = property(is_edited)
