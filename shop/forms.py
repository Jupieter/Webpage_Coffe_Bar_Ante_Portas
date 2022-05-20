from email.policy import default
from django import forms
from .models import CoffeeMake
from django.utils import timezone
import datetime




class CoffeeMaker(forms.Form):

    c_make_ware = forms.ChoiceField(
        label='Bontott kávé:'
    )

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
    c_make_date = forms.DateField(
        label='Főzés napja:',
        initial = timezone.now(),
        widget = forms.DateInput(
            format=('%Y.%m.%D'),
            attrs={
                "class": "form-control dateinput ",               
                "type":"date"
                }
            ),
    )

    c_make_time = forms.TimeField(
        label='Főzés ideje:',
        initial = timezone.now(),
        widget=forms.TimeInput(
            format=('%H:%M'),
            attrs={
                "class": "form-control",               
                "type":"time"
                }
            ),
    )
 
        #class Meta:             fields = ('c_make_dose', 'c_make_date', 'c_make_time', 'c_make_datetime')

        

    
    
     