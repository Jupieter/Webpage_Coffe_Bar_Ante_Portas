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
    ware_weight= models.IntegerField(verbose_name='Csomag tömege [g]', default=0)
    ware_price = models.IntegerField(verbose_name='Csomag ára [Ft]',default=0)
    pub_date = models.DateTimeField('Rögzítés dátuma', default=timezone.now)
    
    def __str__(self):
        w_name_1 = self.ware_type 
        w_name_2 = self.ware_brand 
        w_name_3 = self.ware_brand_name 
        ware_name = str(w_name_2) + ', ' + str(w_name_3) + ', ' + str(w_name_1)
        return ware_name
       

class StatusChoise(models.IntegerChoices):
    MINDEGYIK = 0
    BESZEREZVE  = 1
    RAKTÁRON = 2
    KIBONTVA = 3
    ELFOGYOTT = 4


class ProductAcquisition(models.Model):
    ware_type = models.ForeignKey(
        WareData, 
        on_delete=models.CASCADE, 
        related_name = 'Áru', 
        verbose_name = 'Áru')
    store_status = models.IntegerField(default=0, choices=StatusChoise.choices, verbose_name="Raktározási státusz")
    acquisition_price = models.IntegerField(default=0, verbose_name='Ára [Ft]')

    acquisiton_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Beszerző', 
        verbose_name = 'Beszerző',
        default=User)
    acquisition_date = models.DateTimeField(
        verbose_name='Beszerzés dátuma', 
        null=True, blank=True,)

    store_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Bevételezte',
        verbose_name ='Bevételezte' )
    store_date = models.DateTimeField(
        verbose_name='Raktározás dátuma', 
        null=True, blank=True,)
    stock = models.IntegerField(default=0, verbose_name='Készleten [g]')

    open_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Kibontotta',
        verbose_name ='Kibontotta' )
    open_date = models.DateTimeField(
        verbose_name='Kibontás dátuma', 
        null=True, blank=True,)
    
    empty_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Leírta',
        verbose_name ='Leírta' )
    empty_date = models.DateTimeField(
        verbose_name='Kifogyás dátuma', 
        null=True, blank=True,)
    
    def __str__(self):
         p_acq_name = str(self.ware_type) + ", " + str(self.id)
         return p_acq_name
