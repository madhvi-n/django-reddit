"""
ASGI config for reddit_clone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application

from env_settings import configure_environment

configure_environment()
application = get_asgi_application()
