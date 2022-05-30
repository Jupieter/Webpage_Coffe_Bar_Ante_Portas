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
        # initial=datetime.datetime.today(),        
        widget = forms.DateTimeInput(
            # format=('%Y.%m.%D'),
            attrs={
                "class": "form-control",               
                "type":"date"
                }
            )
    )
    c_make_time = forms.TimeField(
        label='Elkészül:',
        # initial = datetime.datetime.now(),   #.isoformat(timespec='minutes'),
        widget=forms.TimeInput(
            # format=('%H:%M'),
            attrs={
                "class": "form-control",               
                "type":"time"
                }
            ),
    )
 
    class Meta:             
        fields = ('c_make_dose', 'c_make_date', 'c_make_time',)

class CoffeeOrderForm(forms.ModelForm):
    class Meta:
        model = CoffeeOrder
        fields = ('coffee_dose','sugar_dose', 'milk_dose','flavour_dose')        
        widgets = {
            'coffee_dose': forms.NumberInput(attrs={'id':'coffeeRange', 'type':'range', 'min':'0', 'step':'0.5', 'max':'2'}),
            'sugar_dose': forms.NumberInput(attrs={'id':'sugarRange', 'type':'range', 'min':'0', 'step':'0.5', 'max':'3'}),
            'milk_dose': forms.NumberInput(attrs={ 'id':'milkRange','type':'range', 'min':'0', 'step':'0.5', 'max':'4'}),
            'flavour_dose': forms.NumberInput(attrs={ 'id':'flavourRange','type':'range', 'min':'0', 'step':'0.5', 'max':'2'}),
        }
    
     