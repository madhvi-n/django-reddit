import random
import secrets
import string

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from groups.models import Group, GroupMember


class Command(BaseCommand):
    help = "Populate users as moderators and moderators in groups if exist"

    def generate_password(self):
        password = None
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))
        return password

    def handle(self, *args, **options):
        API_ENDPOINT = "https://dummyjson.com/users?limit=100"
        response = requests.get(API_ENDPOINT)
        users = response.json()["users"]
        for user in users:
            group_id = user.get("id") % 5
            user, created = User.objects.get_or_create(
                first_name=user.get("firstName"),
                last_name=user.get("lastName"),
                email=user.get("email"),
                username=user.get("username") + str(group_id),
                password=self.generate_password(),
            )
            try:
                member_type = random.choices(["MEMBER", "MODERATOR"])
                group = Group.objects.get(id=group_id)
                member, created = GroupMember.objects.get_or_create(
                    user=user, member_type=member_type, group=group
                )
            except Group.DoesNotExist:
                pass
        print()
