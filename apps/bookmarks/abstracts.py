from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models


class AbstractBookmark(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        ordering = [
            "created_at",
        ]
