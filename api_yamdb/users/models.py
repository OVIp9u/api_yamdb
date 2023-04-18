from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': ('Пользователь уже существует')
        }
    )
    email = models.EmailField('Email адрес', max_length=254, unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField('Код подтверждения', max_length=6)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username

    @property
    def is_moderator_role(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin_role(self):
        return (
            self.role == self.Role.ADMIN or self.is_superuser or self.is_staff
        )
