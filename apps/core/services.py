import os

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        return None


def mail(subject, email_template, recipient, context):
    pass
