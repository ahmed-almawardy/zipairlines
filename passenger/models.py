from django.db import models
from django.utils.translation import gettext as _


class Passenger(models.Model):
    name = models.CharField(_('name'), null=True, blank=True, max_length=250)
    email = models.CharField(_('email'), null=True, blank=True, max_length=250)
    phone = models.CharField(_('phone'), null=True, blank=True, max_length=250)
    
    def __str__(self) -> str:
        return self.name