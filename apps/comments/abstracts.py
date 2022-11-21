from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import TimeStampedModel


class AbstractComment(TimeStampedModel):
    user = models.ForeignKey(
        User, null=True,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name="%(class)s_comments",
    )
    _comment = models.TextField(max_length=3000)
    is_removed = models.BooleanField(
        default=False,
        help_text='Check this box if the comment is inappropriate. '
            'A "This comment has been removed" message will '
            'be displayed instead.'
    )
    is_nesting_permitted = models.BooleanField(
        default=False
    )
    flair = models.TextField(blank=True, max_length=50)
    mentioned_users = models.ManyToManyField(
        User, blank=True,
        related_name="%(class)s_mentions",
        verbose_name='mentioned_users'
    )

    class Meta:
        abstract = True
        ordering = ['created_at',]

    def _get_comment(self):
        comment = self._comment
        if self.is_removed:
            comment = "This comment has been removed"
        return comment
    comment = property(_get_comment)


class AbstractCommentVote(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_votes"
    )

    vote = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-1), MaxValueValidator(1)]
    )

    class Meta:
        abstract = True
