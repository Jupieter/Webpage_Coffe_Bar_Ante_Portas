from rest_framework import serializers
from shop.models import *

class CoffeeMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMake
        fields = '__all__'