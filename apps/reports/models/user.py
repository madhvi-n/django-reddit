from django.db import models

from reports.abstracts import AbstractReport
from django.contrib.auth.models import User


class UserProfileReport(AbstractReport):
    reported_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    class Meta:
        ordering = ['-created_at',]
        verbose_name = 'User Profile Report'
        verbose_name_plural = 'User Profile Reports'

    def __str__(self):
        return f"Report: {self.reported_user.username} by {self.reporter.username}"
