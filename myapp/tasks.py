from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_message_about_changes(lesson, email):
    send_mail(
        subject='Обновление по курсу!',
        message=f'Курс {lesson} был обновлён!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email
    )
    print("send check")
