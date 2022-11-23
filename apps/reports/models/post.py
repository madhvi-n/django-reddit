from django.db import models

from reports.abstracts import AbstractReport
from posts.models import Post


class PostReport(AbstractReport):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'Post Report'
        verbose_name_plural = 'Post Reports'

    def __str__(self):
        return f"Report: {self.reported_user.username} by {self.reporter.username}"
