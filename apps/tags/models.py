from django.db import models
from core.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return str(self.name)
