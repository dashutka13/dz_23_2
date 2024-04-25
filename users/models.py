from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    verify_key = models.CharField(**NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='статус аккаунта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
