from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models


class AbstractFollower(TimeStampedModel):
    follower = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE,
        related_name="%(class)s_followers",
    )

    class Meta:
        abstract = True
