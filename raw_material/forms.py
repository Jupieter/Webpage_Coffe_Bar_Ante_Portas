from django import forms
from .models import WareData, ProductAcquisition
from django.utils import timezone


class WareDataForm(forms.ModelForm):
    class Meta:
        model = WareData
        fields = ('ware_type','ware_brand', 'ware_brand_name','ware_weight','ware_price')


class AquisitionForm(forms.ModelForm):
    class Meta:
        model = ProductAcquisition
        fields = ('acquisitor_user', 'acquisition_date',)
    # acquisition_date = forms.DateField(required=True, label='Beszerezve:', initial=timezone.now)
    # stock = forms.IntegerField(required=True, label='Készlet [g]')

    