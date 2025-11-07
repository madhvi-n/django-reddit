from core.models import TimeStampedModel
from django.db import models


class ReportType(TimeStampedModel):
    title = models.TextField(max_length=200)
    info = models.TextField(blank=True)

    class Meta:
        verbose_name = "Report Type"
        verbose_name_plural = "Report Types"

    def __str__(self):
        return f"{self.title}"
