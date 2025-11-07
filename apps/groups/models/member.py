from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from groups.models import Group


class GroupMember(TimeStampedModel):

    class MemberTypes(models.TextChoices):
        ADMIN = "ADMIN"
        MODERATOR = "MODERATOR"
        MEMBER = "MEMBER"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        BANNED = "BANNED"
        MUTED = "MUTED"

    group = models.ForeignKey(Group, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    member_type = models.CharField(
        choices=MemberTypes.choices,
        max_length=10,
        default=MemberTypes.MEMBER,
        help_text="""
            ADMIN: Has (all)permissions to add or remove members as moderators, ban or mute members.<br>
            MODERATOR: Has permission to add, remove, ban or mute members.<br>
            MEMBER: Can post, like, comment, share, bookmark group posts.
        """,
    )
    status = models.CharField(
        choices=Status.choices,
        max_length=10,
        default=Status.ACTIVE,
        help_text="""
            ACTIVE: Can be active in a group within permissions.<br>
            MUTED: Forbidden for any activity(post, comment etc) in a group for a week.<br>
            BANNED: Forbidden for any activity in a group forever
        """,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Group Member"
        verbose_name_plural = "Group Members"

    def __str__(self):
        return f"{self.user.username} added to {self.group.name} as {self.member_type}"
