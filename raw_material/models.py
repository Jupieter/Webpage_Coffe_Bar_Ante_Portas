from django.db import models


class WareData(models.Model):
    ware_type = models.CharField(max_length=50)
    ware_brand = models.CharField(max_length=50)
    ware_brand_name = models.CharField(max_length=50)
    package_weight= models.IntegerField(default=0)
    ware_price = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')


class ProductIngredient(models.Model):
    product_name = models.CharField(max_length=50)
    material1 = models.IntegerField(default=0)
    material2 = models.IntegerField(default=0)
    material3 = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
