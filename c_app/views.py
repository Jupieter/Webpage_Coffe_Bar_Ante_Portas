# django-rest authentication
import datetime
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# knox token authentication
from rest_framework import generics, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
# from .serializers import UserSerializer, RegisterSerializer
from .serializers import *
from  shop.models import *
from  shop.views import active_coffee, dose_weight
from  .models import *

def dt_coffee_make(hourS=1):
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=hourS)
    print(dt_start)
    print(dt_end)
    tasks1 = CoffeeMake.objects.filter(c_make_date__range=(dt_start, dt_end))
    tasks = tasks1.order_by('c_make_date')
    return tasks


# Create your views here.
@api_view(['GET'])
def active_coffe_ware(request):
    act_ware = active_coffee()
    dose_wgt = dose_weight(1)
    print(act_ware, ':', dose_wgt)
    coffe_ware = []
    for ware in act_ware:
        w_id = ware.id
        w_name = str(ware.ware_type)
        w_dose = int(ware.stock / dose_wgt)
        print(w_id, w_name, w_dose)
        i = {"w_id":w_id,"w_name":w_name,"w_dose":w_dose}
        i_json = json.dumps(i)
        coffe_ware.append(i_json)
    data = coffe_ware
    print(data)
    # serializer = ActiveCoffeeSerializer(act_ware, many=True)
    # rint(serializer.data)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def todaytcoffee(request):
    tasks = dt_coffee_make(20)
    print(tasks)
    serializer = FirstCoffeeSerializer(tasks, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def c_make(request):
    tasks = dt_coffee_make(20)
    serializer = CoffeeMakeSerializer(tasks, many=True)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_tasks(request):
    tasks = Task.objects.all()
    # print(tasks)
    serializer = TaskSerializer(tasks, many=True)
    print('GET: ',serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def create_task(request):
    data = request.data
    print('POST: ', data)
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        ser_data = serializer.data
        Task.objects.create(name=ser_data['name'])
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        print('r: ', request)
        serializer = MyAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print('u: ', user)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
# https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
# https://james1345.github.io/django-rest-knox/

@api_view(['POST'])
def logins(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Succesfully login"
            data['email'] = account.email
            data['password'] = account.password
        else:
            data = serializer.error        
        return Response(data, status=status.HTTP_200_OK)