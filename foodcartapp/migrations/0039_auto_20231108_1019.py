# Generated by Django 3.2.15 on 2023-11-08 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone_number',
            new_name='phonenumber',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='count',
            new_name='quantity',
        ),
    ]