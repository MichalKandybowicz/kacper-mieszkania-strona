from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Apartment(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Dostępne'
        RESERVED = 'reserved', 'Zarezerwowane'
        SOLD = 'sold', 'Sprzedane'

    number = models.PositiveSmallIntegerField(
        'numer mieszkania', unique=True, validators=[MinValueValidator(1)]
    )
    title = models.CharField('nazwa', max_length=120)
    area = models.DecimalField(
        'powierzchnia (m²)', max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    rooms = models.PositiveSmallIntegerField(
        'liczba pokoi', validators=[MinValueValidator(1)]
    )
    floor = models.PositiveSmallIntegerField('piętro', default=0)
    price = models.DecimalField(
        'cena (zł)', max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    description = models.TextField('opis')
    status = models.CharField(
        'status', max_length=10, choices=Status.choices, default=Status.AVAILABLE
    )

    class Meta:
        ordering = ['number']
        verbose_name = 'mieszkanie'
        verbose_name_plural = 'mieszkania'

    def __str__(self):
        return f'M{self.number} — {self.title}'

    def get_absolute_url(self):
        return reverse('offers:detail', kwargs={'pk': self.pk})
