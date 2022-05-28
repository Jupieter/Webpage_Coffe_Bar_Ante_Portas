from django.db import models
from django.utils import timezone
from accounts.models import User
from raw_material.models import WareData, ProductAcquisition
# Create your models here.

class CoffeeMake(models.Model):
    c_make_ware = models.ForeignKey(ProductAcquisition, on_delete=models.CASCADE, verbose_name='Kávé fajta')
    c_make_dose = models.IntegerField(verbose_name='Adag', default=4)
    c_make_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Lefőzte', 
        verbose_name = 'Lefőzte',
        default=User)
    c_make_date = models.DateTimeField('Elkészül:', null=True, blank=True)
    c_reg_time = models.DateTimeField('Rögzítés dátuma', default=timezone.now)

class CoffeeOrder(models.Model):
    coffee_selected = models.ForeignKey(CoffeeMake, on_delete=models.CASCADE, verbose_name='Lefoglalt Kávé')
    coffee_dose = models.IntegerField(verbose_name='Kávé [0,5-2] Adag', default=1)
    sugar_dose =  models.IntegerField(verbose_name='Cukor [0,5-3] Adag [5 g]', default=1)
    milk_dose =  models.IntegerField(verbose_name='Tej [0,5-4] Adag [50 ml]', default=1)
    flavour_dose =  models.IntegerField(verbose_name='Ízesítő [0,5-2] Adag [5 g]', default=1)
    coffe_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Lefoglalta', 
        verbose_name = 'Lefoglalta',
        default=User)
    coffee_reg = models.DateTimeField('Rögzítés dátuma', default=timezone.now)