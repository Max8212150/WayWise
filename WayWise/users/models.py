from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    father_name = models.CharField(
        verbose_name='Отчество',
        max_length=40,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'    

    def __str__(self):
        return f"{self.username} ({self.email})"
