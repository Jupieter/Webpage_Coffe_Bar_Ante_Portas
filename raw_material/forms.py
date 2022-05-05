from django import forms

from .models import WareData

class WareDataForm(forms.ModelForm):

    class Meta:
        model = WareData
        fields = ('ware_brand', 'ware_brand_name','ware_weight','ware_price')