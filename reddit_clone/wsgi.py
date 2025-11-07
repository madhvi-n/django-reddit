"""
WSGI config for reddit_clone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from env_settings import configure_environment

configure_environment()
application = get_wsgi_application()
