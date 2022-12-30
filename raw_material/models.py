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
    ware_brand = models.CharField(verbose_name='Brand', max_length=50,)
    ware_brand_name = models.CharField(verbose_name='Type', max_length=50)
    ware_weight= models.IntegerField(verbose_name='Package weight [g]', default=0)
    ware_price = models.IntegerField(verbose_name='Package price [Ft]',default=0)
    pub_date = models.DateTimeField('Record date', default=timezone.now)
    
    def __str__(self):
        w_name_1 = self.ware_type 
        w_name_2 = self.ware_brand 
        w_name_3 = self.ware_brand_name 
        ware_name = str(w_name_2) + ', ' + str(w_name_3) + ', ' + str(w_name_1)
        return ware_name
       

class StatusChoise(models.IntegerChoices):
    ALL = 0
    ACQUIRED  = 1
    IN_WAREHOUSE = 2
    EXPANDED = 3
    SOLD_OUT = 4


class ProductAcquisition(models.Model):
    ware_type = models.ForeignKey(
        WareData, 
        on_delete=models.CASCADE, 
        related_name = 'Product', 
        verbose_name = 'Product ty')
    store_status = models.IntegerField(default=0, choices=StatusChoise.choices, verbose_name="Storage status")
    acquisition_price = models.IntegerField(default=0, verbose_name='Price [Ft]')

    acquisiton_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=False, 
        related_name ='Purchaser', 
        verbose_name = 'Purchaser Person',
        default=User)
    acquisition_date = models.DateTimeField(
        verbose_name='Purchase date', 
        null=True, blank=True,)

    store_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Store_booking_person',
        verbose_name ='Store booking person' )
    store_date = models.DateTimeField(
        verbose_name='Store date', 
        null=True, blank=True,)
    stock = models.IntegerField(default=0, verbose_name='In stock [g]')

    open_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Opening_booking_person',
        verbose_name ='Opening booking person' )
    open_date = models.DateTimeField(
        verbose_name='Opening date', 
        null=True, blank=True,)
    
    empty_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name = 'Expiry_booking_person',
        verbose_name ='Expiry booking person' )
    empty_date = models.DateTimeField(
        verbose_name='Expiry date', 
        null=True, blank=True,)
    
    def __str__(self):
         p_acq_name = str(self.ware_type) + ", " + str(self.id)
         return p_acq_name
