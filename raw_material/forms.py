from django import forms
from .models import WareData, ProductAcquisition


class WareDataForm(forms.ModelForm):
    class Meta:
        model = WareData
        fields = ('ware_type','ware_brand', 'ware_brand_name','ware_weight','ware_price')


class AquisitionForm(forms.ModelForm):
    class Meta:
        model = ProductAcquisition
        fields = ('ware_type', 'acquisitor_user', 'acquisition_date', 'acquisition')