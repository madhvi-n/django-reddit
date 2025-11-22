from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from groups.models import Group


class MemberRequest(TimeStampedModel):
    group = models.ForeignKey(
        Group, related_name="member_requests", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="requested_groups", on_delete=models.CASCADE
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Member Request"
        verbose_name_plural = "Member Requests"

    def __str__(self):
        return f"{self.user.username} sent a request to join {self.group.name}"
