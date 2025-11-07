import uuid

from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from tags.models import Tag


class Group(TimeStampedModel):
    class Type(models.TextChoices):
        PUBLIC = "PUBLIC"
        RESTRICTED = "RESTRICTED"
        PRIVATE = "PRIVATE"

    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    group_type = models.CharField(
        choices=Type.choices,
        max_length=15,
        default=Type.PUBLIC,
        help_text="""
            PUBLIC: Anyone can view, post, and comment to this community.<br>
            RESTRICTED: Anyone can view this community, but only approved users can post.<br>
            PRIVATE: Only approved users can view and submit to this community.
        """,
    )
    archive_posts = models.BooleanField(
        default=False,
        help_text="Posts after a period of X months will be archived automatically",
    )
    topics = models.ManyToManyField(
        Tag, blank=True, verbose_name="topics", related_name="groups"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return f"Group: {self.name}"
