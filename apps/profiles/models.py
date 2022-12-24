from django.db import models

from core.models import TimeStampedModel
from django.contrib.auth.models import User
from tags.models import Tag


class UserMetaInfo(TimeStampedModel):
    user = models.OneToOneField(
        User,
        verbose_name="user",
        related_name="meta_info",
        on_delete=models.CASCADE
    )
    username_changed = models.DateField(
        null=True, blank=True,
        verbose_name="username_changed",
    )
    bio = models.TextField(blank=True)
    dob = models.DateField(null=True)
    dob_visible = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_requesting_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Meta Info"
        verbose_name_plural = "User Meta Info"

    def __str__(self):
        return f"Profile Info: {self.username}"
