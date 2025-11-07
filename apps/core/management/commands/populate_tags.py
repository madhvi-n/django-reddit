from django.core.management.base import BaseCommand, CommandError

from tags.models import Tag, TagType

import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Populate Tag and TagType from the CSV provided'

    def handle(self, *args, **options):
        for type in ["INTEREST", "GENERAL", "TOPIC"]:
            TagType.objects.create(title=type)

        path = Path('tags.csv').absolute()
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name'].title()
                type = row[' type'].lstrip().rstrip().upper()
                tag_type = TagType.objects.get(title=type)
                tag, created = Tag.objects.get_or_create(
                    name=name, tag_type=tag_type
                )
