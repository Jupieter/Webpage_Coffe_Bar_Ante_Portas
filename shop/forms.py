from email.policy import default
from django import forms
from .models import CoffeeMake, CoffeeOrder
from django.utils import timezone
import datetime, time


class CoffeeMakerForm(forms.Form):
    c_make_dose = forms.IntegerField(
        label='Lefőzött kávé adag:',
        max_value = 8,
        min_value = 0,
        initial = 4,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Lefőzött kávé adag",
                }
            )
    )
    c_make_date = forms.DateTimeField(
        label='Főzés napja:', 
        widget = forms.DateTimeInput(
            attrs={
                "class": "form-control",               
                "type":"date"
                }
            )
    )
    c_make_time = forms.TimeField(
        label='Elkészül:',
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",               
                "type":"time"
                }
            ),
    ) 
    class Meta:             
        fields = ('c_make_dose', 'c_make_date', 'c_make_time',)

class CoffeeTimeForm(forms.Form):
    c_make_date = forms.DateTimeField(
    label='Főzés napja:', 
    widget = forms.DateTimeInput(
        attrs={
            "class": "form-control",               
            "type":"date"
            }
        )
    )
    c_make_time = forms.TimeField(
        label='Elkészül:',
        widget=forms.TimeInput(
            attrs={
                "class": "form-control",               
                "type":"time"
                }
            ),
    ) 
    class Meta:             
        fields = ('c_make_date', 'c_make_time',)

class CoffeeOrderForm(forms.ModelForm):
    class Meta:
        model = CoffeeOrder
        fields = ('coffee_dose','sugar_dose', 'sugar_choice', 'milk_dose','milk_choice', 'flavour_dose', 'flavour_choice')        
        widgets = {
            'coffee_dose': forms.NumberInput(attrs={'id':'coffeeRange', 'type':'range', 'min':'0.5', 'step':'0.5', 'max':'2'}),
            'sugar_dose': forms.NumberInput(attrs={'id':'sugarRange', 'type':'range', 'min':'0', 'step':'0.5', 'max':'3'}),
            'milk_dose': forms.NumberInput(attrs={ 'id':'milkRange','type':'range', 'min':'0', 'step':'0.5', 'max':'4'}),
            'flavour_dose': forms.NumberInput(attrs={ 'id':'flavourRange','type':'range', 'min':'0', 'step':'0.5', 'max':'2'}),
        }
        # exclude = ['sugar_choice', 'milk_choice', 'flavour_choice']
    
     