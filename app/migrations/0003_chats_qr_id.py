# Generated by Django 4.2.3 on 2023-07-06 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_chats_last_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='qr_id',
            field=models.CharField(default='none', max_length=256, verbose_name='ID qr для телеграмма'),
        ),
    ]
