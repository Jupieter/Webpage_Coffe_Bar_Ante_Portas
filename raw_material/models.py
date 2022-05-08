from django.db import models
from django.utils import timezone

# Create your models here.


class WareTypes(models.Model):
    ware_types = models.CharField(verbose_name='Anyag fajta',max_length=10,)
    ware_wght= models.IntegerField(verbose_name='Egységnyi tömeg [g]', default=0)
    
    def __str__(self):
        return self.ware_types

    class Meta:
        ordering = ['ware_types']    


class WareData(models.Model):
    ware_type = models.ForeignKey(WareTypes, on_delete=models.CASCADE)
    ware_brand = models.CharField(verbose_name='Márkája', max_length=50,)
    ware_brand_name = models.CharField(verbose_name='Fajtája', max_length=50)
    ware_weight= models.IntegerField(verbose_name='Csomag tömege [g]', default=0)
    ware_price = models.IntegerField(verbose_name='Csomag ára [g]',default=0)
    pub_date = models.DateTimeField('Rögzítés dátuma', default=timezone.now)


class ProductIngredient(models.Model):
    product_name = models.CharField(max_length=50)
    material1 = models.IntegerField(default=0)
    material2 = models.IntegerField(default=0)
    material3 = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

