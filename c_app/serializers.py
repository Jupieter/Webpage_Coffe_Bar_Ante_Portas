from rest_framework import serializers
from shop.models import *
from django.contrib.auth.models import User
from accounts.models import *

class CoffeeMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMake
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'], 
            validated_data['password']
            )
        return user