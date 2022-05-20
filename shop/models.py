from django.db import models
from django.utils import timezone
from accounts.models import User
from raw_material.models import WareData, ProductAcquisition
# Create your models here.

class CoffeeMake(models.Model):
    c_make_ware = models.ForeignKey(ProductAcquisition, on_delete=models.CASCADE, verbose_name='Kávé fajta')
    c_make_dose= models.IntegerField(verbose_name='Adag', default=4)
    c_reg_time = models.DateTimeField('Rögzítés dátuma', default=timezone.now)
    c_make_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Lefőzte', 
        verbose_name = 'Lefőzte',
        default=User)
    c_make_datetime = models.DateTimeField('Elkészül:', default=0, null=True, blank=True,)
