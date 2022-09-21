from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AbstractVote(TimeStampedModel):
    user = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name="%(class)s_votes",
    )
    vote = models.IntegerField(
        default=0,
        validators=[MinValueValidator(-1), MaxValueValidator(1)]
    )

    class Meta:
        abstract = True
