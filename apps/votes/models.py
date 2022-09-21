from django.db import models
from comments.models import PostComment
from posts.models import Post

from .abstracts import AbstractVote


class PostVote(AbstractVote):
    post = models.ForeignKey(
        Post,
        verbose_name="post",
        on_delete=models.CASCADE,
        related_name="votes"
    )

    class Meta:
        verbose_name = "Post Vote"
        verbose_name_plural = "Post Votes"

    def __str__(self):
        return "Vote on " + str(self.post.uuid) + " by " + str(self.user.username)


class PostCommentVote(AbstractVote):
    post_comment = models.ForeignKey(
        PostComment,
        verbose_name="comment",
        on_delete=models.CASCADE,
        related_name="votes"
    )

    class Meta:
        verbose_name = "Post Comment Vote"
        verbose_name_plural = "Post Comment Votes"

    def __str__(self):
        return "Vote on " + str(self.post_comment.id) + " by " + str(self.user.username)
