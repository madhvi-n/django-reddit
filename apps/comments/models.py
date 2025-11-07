from comments.abstracts import AbstractComment, AbstractCommentVote
from django.db import models
from django.db.models import Sum
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
        return f"Comment: {self.post.title} by {self.user.username}"

    def _get_score(self):
        score = 0
        votes = PostCommentVote.objects.filter(post_comment=self)
        if votes.exists():
            score = votes.aggregate(Sum('vote'))['vote__sum'] or 0
        return score
    score = property(_get_score)


class PostCommentVote(AbstractCommentVote):
    post_comment = models.ForeignKey(
        PostComment,
        on_delete=models.CASCADE,
        related_name="votes"
    )

    class Meta:
        ordering = ['created_at',]
        verbose_name = "Post Comment Vote"
        verbose_name_plural = "Post Comment Votes"

    def __str__(self):
        return f"{self.vote} point by {self.user.username}"
