from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db import models
from reports.models.types import ReportType


class AbstractReport(TimeStampedModel):
    class STATUS(models.TextChoices):
        INITIATED = "INITIATED"
        VERIFIED = "VERIFIED"
        RESOLVED = "RESOLVED"
        REJECTED = "REJECTED"
        REDACTED = "REDACTED"

    STATUS_HELP_TEXT = """
        1. Anyone can create a report. Does not mean it is valid
        2. Report is valid and further actions can be taken.
        3. The Report was verified but is no longer valid. The problem has been solved.
        4. Verified and found the report has no basis. Fake/ Invalid.
        5. User is withdrawing the report.
    """

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_reports",
    )
    report_type = models.ForeignKey(
        ReportType,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_reports",
    )
    url = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default="INITIATED",
        help_text=STATUS_HELP_TEXT,
    )

    class Meta:
        abstract = True
        ordering = [
            "created_at",
        ]
