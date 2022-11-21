from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from core.models import TimeStampedModel
from tags.models import Tag
from django.core.validators import MinValueValidator, MaxValueValidator
from groups.models import Group
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
    group = models.ForeignKey(
        Group, null=True, blank=True,
        related_name="posts",
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post: {self.uuid} published by {self.author.username}"

    def _get_score(self):
        score = 0
        votes = PostVote.objects.filter(post=self)
        if votes.exists():
    	    score = votes.aggregate(Sum('vote'))['vote__sum'] or 0
        return score
    score = property(_get_score)


class PostVote(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="post_votes"
    )

    vote = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-1), MaxValueValidator(1)]
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    class Meta:
        ordering = ['created_at',]
        verbose_name = "Post Vote"
        verbose_name_plural = "Post Votes"

    def __str__(self):
        return f"{self.vote}  point by  {self.user.username}"
