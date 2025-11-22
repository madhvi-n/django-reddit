from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from groups.models import Group


class GroupRule(TimeStampedModel):
    class RuleType(models.TextChoices):
        POSTS = "POSTS"
        COMMENTS = "COMMENTS"
        BOTH = "BOTH"

    group = models.ForeignKey(Group, related_name="rules", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    rule_type = models.CharField(
        choices=RuleType.choices, max_length=10, default=RuleType.BOTH
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Group Rule"
        verbose_name_plural = "Group Rules"

    def __str__(self):
        return f"{self.group.name} rule : {self.title[:40]}"
