from rest_framework import serializers
from .models import *
from shop.models import *
from raw_material.models import *
from django.contrib.auth.models import User
from accounts.models import *


from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class CoffeFriend(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ActiveCoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAcquisition
        fields = '__all__'


class FirstCoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMake
        fields = '__all__'


class CoffeeOrderSerializerSave(serializers.ModelSerializer):
    class Meta:
        model = CoffeeOrder
        fields = '__all__'
        # fields = ['coffee_selected', 'coffee_dose', 'coffe_user', 'sugar_choice', 'sugar_dose', 'milk_choice', 'milk_dose', 'flavour_choice', 'flavour_dose']
        # fields = ['coffee_selected', 'coffee_dose', 'sugar_choice', 'sugar_dose', 'milk_choice', 'milk_dose', 'flavour_choice', 'flavour_dose', 'coffe_user', coffee_reg]



class CoffeeMakeSerializerSave(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMake
        fields = ['c_make_user', 'c_make_dose','c_make_date','c_make_ware']
        # fields = ['c_make_ware', 'c_make_dose', 'c_make_user', 'c_make_date', 'c_reg_time']


class CoffeeMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMake
        fields = ['c_make_date']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        print('attrs',attrs)
        return attrs


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'], 
            validated_data['password']
            )
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'