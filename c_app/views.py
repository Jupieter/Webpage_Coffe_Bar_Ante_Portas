import json
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from  shop.models import *

# Create your views here.
@api_view(['GET'])
def all_tasks(request):
    tasks = CoffeeMake.objects.all()
    serializer = CoffeeMakeSerializer(tasks, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_task(request):
    data = request.data

    serializer = CoffeeMakeSerializer(data=data)
    if serializer.is_valid():
        ser_data = serializer.data
        CoffeeMake.objects.create(name=ser_data['name'])
        
        return Response(serializer.data, status=status.HTTP_200_OK)