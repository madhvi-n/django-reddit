from django.core.management.base import BaseCommand, CommandError

from reports.models import ReportType

class Command(BaseCommand):
    help = 'Populate Report Types'

    def handle(self, *args, **options):
        types = [
            {
                "title": "Breaks rules",
                "info": "Posts, comments, or behavior that breaks community rules."
            },
            {
                "title": "Harassment",
                "info": "Harassing, bullying, intimidating, or abusing an individual or group of people with the result of discouraging them from participating."
            },
            {
                "title": "Threatening violence",
                "info": "Encouraging, glorifying, or inciting violence or physical harm against individuals or groups of people, places, or animals."
            },
            {
                "title": "Hate",
                "info": "Promoting hate or inciting violence based on identity or vulnerability."
                },
            {
                "title": "Sexualization of minors",
                "info": "Soliciting, sharing, or encouraging the sharing of sexual or suggestive content involving minors or people who appear to be minors."
            },
            {
                "title": "Sharing personal information",
                "info": "Sharing or threatening to share private, personal, or confidential information about someone."
            },
            {
                "title": "Non-consensual intimate media",
                "info": "Sharing, threatening to share, or soliciting intimate or sexually-explicit content of someone without their consent (including fake or 'lookalike' pornography)"
            },
            {
                "title": "Prohibited transaction",
                "info": "Soliciting or facilitating transactions or gifts of illegal or prohibited goods and services."
            },
            {
                "title": "Impersonation",
                "info": "Impersonating an individual or entity in a misleading or deceptive way. This includes deepfakes, manipulated content, or false attributions."
            },
            {
                "title": "Copyright violation",
                "info": "Content posted to Reddit that infringes a copyright you own or control. (Note: Only the copyright owner or an authorized representative can submit a report.)"
            },
            {
                "title": "Spam",
                "info": "Repeated, unwanted, or unsolicited manual or automated actions that negatively affect redditors, communities, and the Reddit platform."
            },
            {
                "title": "Misinformation",
                "info": "Spreading false information such as content that undermines civic processes or provides dangerous health misinformation."
            }
        ]

        for type in types:
            report_type, created = ReportType.objects.get_or_create(
                title=type.get('title'), info=type.get('info')
            )

            print(report_type.id)
            print(report_type.title)
