# Generated by Django 3.2.15 on 2023-11-09 13:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_auto_20231109_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='call_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время звонка'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='registration_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Зарегистрирован'),
        ),
    ]
