from django.db import models
from django.db.models import Sum

from comments.abstracts import AbstractComment
from posts.models import Post


class PostComment(AbstractComment):
    post = models.ForeignKey(
        Post,
        verbose_name='post',
        on_delete=models.CASCADE,
        related_name="comments"
    )

    parent = models.ForeignKey(
        "self", null=True,
        related_name="comments",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['created_at',]
        verbose_name = "Post Comment"
        verbose_name_plural = "Post Comments"

    def __str__(self):
        return "Comment on " + self.post.title + " by " + self.user.username
