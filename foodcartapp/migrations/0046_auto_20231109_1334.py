# Generated by Django 3.2.15 on 2023-11-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('UN', 'Необработанный'), ('AD', 'Принят'), ('RE', 'Готовят'), ('TC', 'Передан курьеру'), ('CO', 'Завершён')], db_index=True, default='UN', max_length=2, verbose_name='Статус'),
        ),
    ]
