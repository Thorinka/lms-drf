from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

from users.models import NULLABLE


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='app/course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(upload_to='app/course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video = models.CharField(max_length=300, verbose_name='ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    METHOD_TRANSACTION = 'transaction'
    METHOD_CASH = 'cash'

    METHODS = (
        (METHOD_TRANSACTION, 'Перевод на счёт'),
        (METHOD_CASH, 'Наличные'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.IntegerField(verbose_name='сумма')
    method = models.CharField(max_length=20, choices=METHODS, default=METHOD_TRANSACTION, verbose_name='метод оплаты')


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    is_active = models.BooleanField(default=True, verbose_name='активен')
