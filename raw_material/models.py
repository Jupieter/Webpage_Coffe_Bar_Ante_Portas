from django.db import models
from django.utils import timezone
from accounts.models import User
# Create your models here.


class WareTypes(models.Model):
    ware_types = models.CharField(verbose_name='Anyag fajta',max_length=10,)
    ware_wght= models.IntegerField(verbose_name='Egységnyi tömeg [g]', default=0)
    ware_image = models.CharField(verbose_name='Ikonja',max_length=100, default='')
    
    def __str__(self):
        return self.ware_types

    class Meta:
        ordering = ['ware_types']    


class WareData(models.Model):
    ware_type = models.ForeignKey(WareTypes, on_delete=models.CASCADE)
    ware_brand = models.CharField(verbose_name='Márkája', max_length=50,)
    ware_brand_name = models.CharField(verbose_name='Fajtája', max_length=50)
    ware_weight= models.IntegerField(verbose_name='Csomag tömege [g]', default=250)
    ware_price = models.IntegerField(verbose_name='Csomag ára [Ft]',default=0)
    pub_date = models.DateTimeField('Rögzítés dátuma', default=timezone.now)
    ware_name = str(ware_brand) + str(ware_brand_name)+ '(' + str(ware_type) + ')'
    
    


class ProductIngredient(models.Model):
    product_name = models.CharField(max_length=50)
    material1 = models.IntegerField(default=0)
    material2 = models.IntegerField(default=0)
    material3 = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

class ProductAcquisition(models.Model):
    ware_type = models.ForeignKey(WareData, on_delete=models.CASCADE, related_name='Áru', verbose_name='Áru' )
    acquisitor_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name='Beszerző', 
        verbose_name= 'Beszerző',
        default=User)
    acquisition = models.BooleanField(default=False, verbose_name='Beszerezve [I/N]')
    acquisition_date = models.DateTimeField(default=timezone.now, verbose_name='Beszerzés dátuma')
    store_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name='Bevételezte',
        verbose_name='Bevételezte'
        )
    stores = models.BooleanField(default=False, verbose_name='Bevételezve [I/N]')
    store_date = models.DateTimeField(default=timezone.now, verbose_name='Raktározás dátuma')
    stock = models.IntegerField(default=0, verbose_name='Készleten [g]')
