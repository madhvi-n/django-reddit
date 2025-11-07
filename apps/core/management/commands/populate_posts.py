from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from posts.models import Post

from .posts import data


class Command(BaseCommand):
    help = "Populate posts using placeholder data"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            for i in range(len(data)):
                new_data = data[i]
                post, created = Post.objects.get_or_create(
                    title=new_data.get("title"),
                    content=new_data.get("content"),
                    author=user,
                )
