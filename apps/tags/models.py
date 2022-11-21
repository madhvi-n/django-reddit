from django.db import models
from core.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class TagType(TimeStampedModel):
    title = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Tag Type'
        verbose_name_plural = 'Tag Types'

    def __str__(self):
        return f"{self.title}"


class Tag(TimeStampedModel):
    name = models.CharField(max_length=30)
    tag_type = models.ForeignKey(
        TagType, null=True,
        verbose_name=_('tag type'),
        related_name="tags",
        on_delete=models.SET_NULL
    )
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f"{self.name}"
