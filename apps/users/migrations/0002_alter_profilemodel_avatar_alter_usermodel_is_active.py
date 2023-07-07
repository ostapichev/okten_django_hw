# Generated by Django 4.2.2 on 2023-07-02 07:07

from django.db import migrations, models

import core.services.upload_avatar_service


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=core.services.upload_avatar_service.upload_avatar),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]