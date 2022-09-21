from django.db import models

from bookmarks.abstracts import AbstractBookmark
from posts.models import Post


class PostBookmark(AbstractBookmark):
    post = models.ForeignKey(
        Post,
        verbose_name="post",
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    class Meta:
        ordering = ['-created_at',]
        unique_together = ['post', 'user']
        verbose_name = 'Post Bookmark'
        verbose_name_plural = 'Post Bookmarks'

    def __str__(self):
        return "Bookmark: " + str(self.blog.title) + " by " +  str(self.user.username)
