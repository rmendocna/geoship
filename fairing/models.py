from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from partial_date import PartialDateField
# Create your models here.


class Ship(models.Model):
    """
    Some attributes taken from https://gisis.imo.org/Public/SHIPS/Default.aspx
    """
    # TODO: flag and ship_type later to be refined with explicit `choices` attribute
    #       or converted to ForeignKeys

    name = models.CharField(max_length=255)
    # NOTE: preferred a surrogate primary key instead of IMO itself.
    #       If it's an overkill, would convert to [a more effective] actual primary key
    imo = models.CharField('IMO', max_length=7, unique=True, db_index=True,
                           validators=[RegexValidator(r'^|\d{7}$')])
    flag = models.CharField(max_length=3, blank=True, help_text='ISO 3-letter code')
    ship_type = models.CharField('Type', max_length=100, blank=True,
                                 help_text='Later refined as a dropdown')
    build = PartialDateField(null=True, blank=True, help_text='year-month')
    mmsi = models.CharField(blank=True, max_length=9, db_index=True, validators=[RegexValidator(r'^|\d{9}$')])

    def str(self):
        s = '%s (IMO %s) %s' % (self.name, self.pk, self.country or '')
        return s.strip()


class ShipPosition(models.Model):
    """
    Plainest way of storing ship location given its IMO
    """
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    class Meta:
        unique_together = [('ship', 'timestamp')]
