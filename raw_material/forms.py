from django import forms
from .models import WareData, ProductAcquisition
from django.utils import timezone


class WareDataForm(forms.ModelForm):
    class Meta:
        model = WareData
        fields = ('ware_type','ware_brand', 'ware_brand_name','ware_weight','ware_price')

class WareListChoice(forms.Form):
    acquisition_list = forms.BooleanField(required=False, label='Beszerezve', initial=True)
    store_list = forms.BooleanField(required=False, label='Raktározva', initial=True)
    opened_list = forms.BooleanField(required=False, label='Kibontva', initial=True)
    empty_list = forms.BooleanField(required=False, label='Elfogyott', initial=False)


class AquisitionForm(forms.ModelForm):
    class Meta:
        model = ProductAcquisition
        fields = ('acquisiton_user', 'acquisition_date',  'acquisition_price',)


class AquisitionStockedForm(forms.ModelForm):
    class Meta:
        model = ProductAcquisition
        fields = ('store_user', )