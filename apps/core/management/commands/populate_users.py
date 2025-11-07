import csv
import random
import secrets
import string

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Populate Users"

    def generate_password(self):
        password = None
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(8))
        return password

    def generate_users(self):
        users = []
        FIRST_NAMES = ["Sally", "Amanda", "Lissie", "John", "Michael", "Andrew"]
        LAST_NAMES = ["Rayburn", "Heart", "Jones", "Phillips", "Barney", "Loid"]
        for i in range(len(FIRST_NAMES)):
            first_name, last_name = random.choice(FIRST_NAMES), random.choice(
                LAST_NAMES
            )
            FIRST_NAMES.remove(first_name)
            LAST_NAMES.remove(last_name)
            users.append(first_name + " " + last_name)
        return users

    def handle(self, *args, **options):
        users = self.generate_users()
        for i in range(len(users)):
            fname, lname = users[i].split()
            email = str(fname + lname).lower() + "@gmail.com"
            user_password = self.generate_password()
            username = fname.lower() + str(random.choice(range(88, 98)))
            user, created = User.objects.get_or_create(
                first_name=fname,
                last_name=lname,
                username=username,
                email=email,
                password=user_password,
            )
