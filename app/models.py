from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Chats(models.Model):
    chat_id = models.CharField(
        verbose_name="Telegram chat id", 
        primary_key=True,
        max_length=56, 
        unique=True
    )
    privat_url = models.CharField(
        verbose_name="Приватная ссылка пользователя",
        max_length=56,
        default="none"

    )
    public_url = models.CharField(
        verbose_name="Публичная ссылка пользователя",
        max_length=56,
        default="none"
    )

    last_callback = models.CharField(
        verbose_name="Последний callback",
        max_length=56,
        default="none"
    )

    last_id = models.CharField(
        verbose_name="Последний callback ID",
        max_length=56,
        default="none"
    )

    qr_id = models.CharField(
        verbose_name="ID qr для телеграмма",
        max_length=256,
        default="none"
    )


    def __str__(self):
        return self.chat_id
    
    class Meta:
        verbose_name = 'Пользователь TG'
        verbose_name_plural = 'Пользователи TG'