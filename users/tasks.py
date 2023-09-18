from celery import shared_task

from users.models import User


@shared_task
def check_last_login():
    users = User.objects.filter(is_active=True, last_login__day__gt=30)
    for user in users:
        user.is_active = False
        user.save()
