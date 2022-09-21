from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from core.models import TimeStampedModel
from tags.models import Tag
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid


class Post(TimeStampedModel):
    class STATUS(models.TextChoices):
        DRAFT = "DRAFT"
        PUBLIC = "PUBLIC"
        ARCHIVED = "ARCHIVED"

    title = models.CharField(max_length=200)
    content = models.TextField(blank=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    author = models.ForeignKey(
        User,
        related_name="posts",
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag, blank=True,
        verbose_name="tags",
        related_name="posts"
    )
    status = models.CharField(
        choices=STATUS.choices,
        default=STATUS.PUBLIC,
        max_length=10
    )
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return f'Post: {self.uuid} by {self.author.username}'
