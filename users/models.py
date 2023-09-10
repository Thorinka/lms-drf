from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
NULLABLE = {
    'blank': True,
    'null': True
}

class UserRoles(models.TextChoices):
    MEMBER = 'member', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default='member')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
