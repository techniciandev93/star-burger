# Generated by Django 3.2.15 on 2023-11-23 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20231121_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='geocoding_failed',
            field=models.BooleanField(default=False, verbose_name='Ошибка геокодинга'),
        ),
    ]
