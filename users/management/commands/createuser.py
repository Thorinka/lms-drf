from django.core.management import BaseCommand

from users.models import User, UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='user@mail.ru',
            first_name='User',
            last_name='Userov',
            role=UserRoles.MEMBER,
            is_superuser=False,
            is_active=True,
            is_staff=False,
        )

        user.set_password('123456')
        user.save()
