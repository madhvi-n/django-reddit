import csv
import random
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from groups.models import Group, GroupMember
from tags.models import Tag, TagType


class Command(BaseCommand):
    help = "Populate groups and group members"

    def handle(self, *args, **options):
        path = Path("groups.csv").absolute()
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["name"].title()
                desc = row[" description"].lstrip().rstrip()
                type = row[" type"].strip()
                topic = row[" topic"].strip()

                tag_type = TagType.objects.filter(title=type).first()
                tag, created = Tag.objects.get_or_create(name=topic, tag_type=tag_type)
                group, created = Group.objects.get_or_create(
                    name=name,
                    description=desc,
                    group_type=type,
                )
                group.topics.add(tag)

                try:
                    user = User.objects.get(id=group.id)
                    admin, created = GroupMember.objects.get_or_create(
                        user=user, group=group, member_type="ADMIN"
                    )
                    print(admin.id)
                except User.DoesNotExist:
                    pass
