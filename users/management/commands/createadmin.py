from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create superuser'

    def handle(self, *args, **options):

        email = input('Enter your email address: ')
        username = input('Enter your username: ')

        while True:
            password = input('Enter your password: ')
            password_confirmation = input('Enter your password again: ')
            if password != password_confirmation:
                print('Passwords do not match')
            else:
                break

        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)
        if not created:
            self.stdout.write(self.style.ERROR("User with such address already exists"))
            return
        user.username = username
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS("Successfully created user"))


