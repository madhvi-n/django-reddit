from core.services import mail
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from reports.models import PostReport, UserProfileReport


@receiver(post_save, sender=PostReport)
def post_reported_mail_hook(sender, instance, created, **kwargs):
    if instance.status == "INITIATED":
        try:
            recipient = settings.HOME_EMAIL
            reporter = instance.reporter
            subject = "Post Report Initiated"
            template_name = "report_initiated_mail.html"
            context = {
                "reporter_name": reporter.first_name + " " + reporter.last_name,
                "reporter_username": reporter.username,
                "object_link": "https://localhost:8000/"
                + str(instance.post.uuid)
                + "/",
                "title": instance.post.title,
                "url": instance.url,
            }
            mail(subject, template_name, recipient, context)
        except:
            pass
        else:
            pass
    if instance.status == "VERIFIED" or instance.report == "REJECTED":
        try:
            recipient = instance.reporter.email
            subject = "Report Progress"
        except:
            pass
        else:
            pass


@receiver(post_save, sender=UserProfileReport)
def user_profile_reported_mail_hook(sender, instance, created, **kwargs):
    if instance.status == "INITIATED":
        try:
            recipient = settings.HOME_EMAIL
            reporter = instance.reporter
            subject = "User Profile Report Initiated"
            template_name = "report_initiated_mail.html"
            context = {
                "reporter_name": reporter.first_name + " " + reporter.last_name,
                "reporter_username": reporter.username,
                "object_link": "http://localhost:8000/"
                + str(instance.reported_user.username)
                + "/",
                "title": instance.reported_user.username,
                "url": instance.url,
            }
            mail(subject, template_name, recipient, context)
        except:
            pass
        else:
            pass
    if instance.status == "VERIFIED" or instance.report == "REJECTED":
        try:
            recipient = instance.reporter.email
            subject = "Report Progress"
        except:
            pass
        else:
            pass
