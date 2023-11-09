# Generated by Django 3.2.15 on 2023-11-09 10:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_alter_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
    ]
