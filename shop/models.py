from django.db import models
from django.utils import timezone
from accounts.models import User
from raw_material.models import WareData, ProductAcquisition
# Create your models here.

class CoffeeMake(models.Model):
    c_make_ware = models.ForeignKey(ProductAcquisition, on_delete=models.CASCADE, verbose_name='Kind of coffee')
    c_make_dose = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Dose', default=4)
    c_make_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Cooked', 
        verbose_name = 'Cooked',
        default=User)
    c_make_date = models.DateTimeField("It's done:", null=True, blank=True)
    c_reg_time = models.DateTimeField('Date recorded', default=timezone.now)
    c_order_yes =models.BooleanField('Have Order', default=False)
    c_book = models.DateTimeField(
        'Accounting Date', 
        blank=True,
        null=True,)

    def __str__(self):
         c_make_name = str(self.c_make_ware) + " / " + str(self.id)
         return c_make_name

class CoffeeOrder(models.Model):
    coffee_selected = models.ForeignKey(CoffeeMake, on_delete=models.CASCADE, verbose_name='Lefoglalt Kávé')
    coffee_dose = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        verbose_name='Kávé [0,5-2] Adag', 
        default=0.5)
    sugar_choice =  models.ForeignKey(
        ProductAcquisition,  
        on_delete=models.SET_NULL,
        related_name = 'strict_sugar',   
        verbose_name='Lefoglalt Cukor',
        blank=True, null=True, unique=False,)   
    sugar_dose =  models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        verbose_name='Cukor [0,5-3] Adag [5 g]', 
        default=0)
    milk_choice =  models.ForeignKey(
        ProductAcquisition,  
        on_delete=models.SET_NULL,
        related_name = 'strict_milk',
        verbose_name='Lefoglalt Tej',
        blank=True, null=True, unique=False,)   
    milk_dose =  models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        verbose_name='Tej [0,5-4] Adag [50 ml]', 
        default=0)
    flavour_choice =  models.ForeignKey(
        ProductAcquisition,  
        on_delete=models.SET_NULL,
        related_name = 'strict_flavour',   
        verbose_name='Lefoglalt Ízesítő',
        blank=True, null=True, unique=False,)  
    flavour_dose =  models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        verbose_name='Ízesítő [0,5-2] Adag [5 g]', 
        default=0)
    coffe_user = models.ForeignKey(
        User, on_delete = models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Lefoglalta', 
        verbose_name = 'Lefoglalta',
        default=User)
    coffee_reg = models.DateTimeField('Rögzítés dátuma', default=timezone.now)

    def __str__(self):
        c_selected = str(self.id) + ":" + str(self.coffee_selected) + ":" + str(self.coffe_user)
        return c_selected
    
    def c_user(self):
        c_user = self.coffe_user
        return c_user
