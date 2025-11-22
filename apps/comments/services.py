from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_mentioned_users(user_id, comment):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        pass
    else:
        comment.mentioned_users.add(user)
        comment.save()
    return comment


def remove_users(user_id, comment):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        pass
    else:
        comment.mentioned_users.remove(user)
        comment.save()
        return comment
