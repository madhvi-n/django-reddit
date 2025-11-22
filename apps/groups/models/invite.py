from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from groups.models import Group


class GroupInvite(TimeStampedModel):
    class InviteAs(models.TextChoices):
        MEMBER = "MEMBER"
        MODERATOR = "MODERATOR"

    group = models.ForeignKey(Group, related_name="invites", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name="invitations", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, related_name="invites", on_delete=models.CASCADE)
    invite_as = models.CharField(
        choices=InviteAs.choices, default=InviteAs.MEMBER, max_length=10
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Group Invite"
        verbose_name_plural = "Group Invites"

    def __str__(self):
        return f"{self.created_by.username} has invited {self.user.username} \
            to join {self.group.name} as a {self.invite_as}."
