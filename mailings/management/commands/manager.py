from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Manager')
        users_data = [
            {'username': 'manager1', 'email': 'manager1@mail.ru', 'password': 'password1'},
            {'username': 'manager2', 'email': 'manager2@mail.ru', 'password': 'password2'},

        ]
        for data in users_data:
            user, created = User.objects.get_or_create(username=data['username'], defaults={
                'email': data['email'],
            })
            if created:
                user.set_password(data['password'])
                user.save()
            group.user_set.add(user)
