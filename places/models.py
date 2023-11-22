from django.db import models


class Place(models.Model):
    address = models.CharField(max_length=150, verbose_name='Адрес', unique=True)
    date = models.DateTimeField(verbose_name='Дата запроса')
    lng = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    lat = models.FloatField(verbose_name='Широта', null=True, blank=True)

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.address
