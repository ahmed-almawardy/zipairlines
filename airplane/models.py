from datetime import datetime
from math import log
from unicodedata import name
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator


class Airplane(models.Model):
    id = models.BigIntegerField(
        unique=True, validators=[MinValueValidator(1), MaxValueValidator(10)], 
        verbose_name=_('id'),
        primary_key=True)
    # type = models.ForeignKey('AirplaneType', on_delete=models.DO_NOTHING)
    # name = models.CharField(_("name"), max_length=250)

    
    @property
    def fuel_tank(self) -> int :
        """
            Each airplane has a fuel tank of (200 liters * id of the airplane) capacity
        """
        return  self.id * settings.FUEL_TANK_LITERS_FRACTION
    
    @property
    def total_fuel_consumption_per_minute(self) -> float:
        """
            we are getting all the registed passengers in the current flight
            we are getting all the registed passengers in the current airplane
            then we are getting them count
            after we are getting the total_fuel_consumption_per_minute by 
            1. additional_consumption = passengers_count * PASSENGER_LITERS_CONSUMPTION_FRACTION
            2. additional_consumption += LITERS_CONSUMPTED_PER_MINUTE
            3. log(self.id) * additional_consumption
        """

        additional_consumption = self.flights.filter(is_active=True).first().passengers.count()\
            * settings.PASSENGER_LITERS_CONSUMPTION_FRACTION
            
        additional_consumption+=settings.LITERS_CONSUMPTED_PER_MINUTE

        return  log(self.id) * additional_consumption

    @property
    def maxmium_minute_to_fly(self) -> int :
        """
            retireving the possible time to fly by calucating fuel tank
            divided by the total  fuel consumption per minute
        """
        return int(self.fuel_tank / self.total_fuel_consumption_per_minute)
    
    def __str__(self) -> str:
        return f'{self.id}'
    

# class AirplaneType(models.Model):
#     name = models.CharField(_('airplane type'), max_length=250)
#     desc = models.TextField(_('type description'), null=True, blank=True)
#     weight = models.PositiveIntegerField(_("weight"), null=True, blank=True)
#     height = models.PositiveIntegerField(_("height"), null=True, blank=True)
    
#     def __str__(self) -> str:
#         return self.name
    

class Flight(models.Model):
    def arrives_default(self) -> datetime:
        from django.utils.timezone import timedelta
        # could make model for destions and the destination between them in m/k 
        # then make an eqution to get a default arrive type depends on the destion_from/to
        return self.deptures + timedelta(hours=2)
    
    name = models.CharField(_("name"), max_length=250)
    passengers = models.ManyToManyField('passenger.Passenger', verbose_name=_('passengers'), related_name='flights')
    airplane = models.ForeignKey('airplane.Airplane', related_name='flights', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(_("is active"), null=True, blank=True, default=False)
    destination_from = models.CharField(_('from'), null=True, blank=True, max_length=250) 
    destination_to = models.CharField(_('to'), null=True, blank=True, max_length=250)
    deptures = models.DateTimeField(_('depture'), auto_now_add=True)
    arrives = models.DateTimeField(_('arrives'), default=arrives_default) 

    def __str__(self) -> str:
        return self.name
    