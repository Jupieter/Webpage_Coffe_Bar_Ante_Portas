# django-rest authentication
import datetime
import json
from urllib import request
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
from  raw_material.models import ProductAcquisition
from  shop.models import *
from  shop.views import active_coffee, dose_weight
from  .models import *


@api_view(['POST'])
def c_order_save(request):
    ''' Save to databse the ordered does & wares'''
    data = request.data
    # print('POST: ', data)
    serializer = CoffeeOrderSerializerSave(data=data)
    # print('serializer: ', serializer)
    if serializer.is_valid():
        ser_data = serializer.data
        #  from string "id" coffee choice --> the object from the database CoffeeMake
        coffee = CoffeeMake.objects.filter(id = ser_data['coffee_selected'])[0]
        ser_data['coffee_selected'] = coffee
        dose = coffee.c_make_dose
        # from string "id" user --> the object from the database User
        user = User.objects.filter(id = ser_data['coffe_user'])[0]
        ser_data['coffe_user'] = user
        # print('user: ', user, type(user))
        # ware choice id type is string --> into object from the database ProductAcquisition
        for wr in ['sugar_choice', 'milk_choice', 'flavour_choice']:
            pk = ser_data[wr]
            # print(ser_data[wr])
            if pk != None and pk != 0:
                ware = ProductAcquisition.objects.filter(id = pk)[0]
            else:
                ware = None
            ser_data[wr] = ware
            # print('ware: ', ware, type(ware))
        # ware dose from string  --> to decimal
        from decimal import Decimal
        for wd in ['coffee_dose', 'sugar_dose', 'milk_dose', 'flavour_dose']:
            w_dose = ser_data[wd]
            w_dose = Decimal(w_dose)
            ser_data[wd] = w_dose

        ser_data['coffee_reg'] = timezone.now()
        serializer.create(ser_data)
        # ordered dose of coffee minus from the possible doses
        coffee.c_make_dose = dose-ser_data["coffee_dose"]
        # print(coffee.c_make_dose, type(coffee.c_make_dose), type(dose), dose, type(ser_data["coffee_dose"]), ser_data["coffee_dose"])
        coffee.save()
    else:
        print('INVALID ') 
    return Response(serializer.data, status=status.HTTP_200_OK)



def coffee_order_data():
    wares = ProductAcquisition.objects.filter(store_status=3)
    coffee = []
    sugar = [json.dumps({"type_id":2, "w_id":0, "w_name":"Zero Sugar", "w_dose":0})]
    milk = [json.dumps({"type_id":2, "w_id":0, "w_name":"Zero Milk", "w_dose":0})]
    flavour = [json.dumps({"type_id":3, "w_id":0, "w_name":"Zero Flavour", "w_dose":0})]
    tasks = dt_coffee_make(60)
    # print(tasks)
    for task in tasks:
            # print(task.c_make_ware.id)
            # print(task.id)
            # print(task.c_make_ware)
            # print(task.c_make_dose)
            c_date = str(task.c_make_date)[0:10]
            c_time = str(task.c_make_date)[11:16]
            # print(c_date)
            # print(c_time)
            c_name = (c_date + "       " + c_time + "\n" + str(task.c_make_ware))
            i = {"type_id": 1, "w_id":task.id, "w_name":c_name, "w_dose":str(task.c_make_dose)}
            i_json = json.dumps(i)
            coffee.append(i_json)
    for ware in wares:
        if ware.ware_type.ware_type.id == 2:
            type_id = ware.ware_type.ware_type.id 
            dose_wgt = dose_weight(type_id)
            w_id = ware.id
            w_name = str(ware.ware_type)
            w_dose = int(ware.stock / dose_wgt)
            # print(w_id, w_name, w_dose)
            i = {"type_id":type_id, "w_id":w_id, "w_name":w_name, "w_dose":w_dose}
            i_json = json.dumps(i)
            sugar.append(i_json)
        elif ware.ware_type.ware_type.id == 3: 
            type_id = ware.ware_type.ware_type.id 
            dose_wgt = dose_weight(type_id)
            w_id = ware.id
            w_name = str(ware.ware_type)
            w_dose = int(ware.stock / dose_wgt)
            # print(w_id, w_name, w_dose)
            i = {"type_id":type_id, "w_id":w_id, "w_name":w_name, "w_dose":w_dose}
            i_json = json.dumps(i)
            milk.append(i_json)
        elif ware.ware_type.ware_type.id == 4: 
            type_id = ware.ware_type.ware_type.id 
            dose_wgt = dose_weight(type_id)
            w_id = ware.id
            w_name = str(ware.ware_type)
            w_dose = int(ware.stock / dose_wgt)
            # print(w_id, w_name, w_dose)
            i = {"type_id":type_id, "w_id":w_id, "w_name":w_name, "w_dose":w_dose}
            i_json = json.dumps(i)
            flavour.append(i_json)
            tastes = [coffee, sugar, milk, flavour]
    return tastes

@api_view(['GET'])
def c_order_data(request):
    data = coffee_order_data()
    return Response(data, status=status.HTTP_200_OK)

def dt_coffee_make(hourS=1):
    # dt= timezone.now()
    dt= datetime.datetime.now()
    dt_start = dt
    dt_end = dt + datetime.timedelta(hours=hourS)
    # print("dt_start", dt_start)
    # print("dt_end", dt_end)
    tasks1 = CoffeeMake.objects.filter(c_make_date__range=(dt_start, dt_end))
    tasks = tasks1.order_by('c_make_date')
    return tasks
    
@api_view(['GET'])
def c_make(request):
    tasks = dt_coffee_make(20)
    serializer = CoffeeMakeSerializer(tasks, many=True)
    # print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def coffe_make(request):
    data = request.data
    #print('POST: ', data)
    serializer = CoffeeMakeSerializerSave(data=data)
    # print('serializer: ', serializer)
    # print('*  *   *   *  *')

    if serializer.is_valid():
        ser_data = serializer.data
        ware = ProductAcquisition.objects.filter(id = ser_data['c_make_ware'])[0]
        user = User.objects.filter(id = ser_data['c_make_user'])[0]
        coffe_new = CoffeeMake(
            c_make_ware = ware,
            c_make_dose = ser_data['c_make_dose'],
            c_make_user = user,
            c_make_date = ser_data['c_make_date'],
            c_reg_time = timezone.now()
            )
        coffe_new.save() 
    else:
        print('INVALID ')    
    return Response(serializer.data, status=status.HTTP_200_OK)


# Create your views here.
@api_view(['GET'])
def active_coffe_ware(request):
    act_ware = active_coffee()
    dose_wgt = dose_weight(1)
    # print(act_ware, ':', dose_wgt)
    coffe_ware = []
    for ware in act_ware:
        w_id = ware.id
        w_name = str(ware.ware_type)
        w_dose = int(ware.stock / dose_wgt)
        # print(w_id, w_name, w_dose)
        i = {"w_id":w_id,"w_name":w_name,"w_dose":w_dose}
        i_json = json.dumps(i)
        coffe_ware.append(i_json)
    data = coffe_ware
    # print(data)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def coffee_notify(request):
    max_id = CoffeeMake.objects.order_by('-id')[0].id
    new_date = CoffeeMake.objects.order_by('-id')[0].c_make_date
    # print(max_id)
    # print(new_date)
    data = {"max_id": max_id, "new_date": new_date}
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def todaytcoffee(request):
    tasks = dt_coffee_make(60)
    serializer = FirstCoffeeSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def next_to_friends(next_cof):
    friends1 = CoffeeOrder.objects.filter(coffee_selected = next_cof)
    friends = []
    for friend in friends1:
        a = str(friend.c_user())
        friends.append(a)
    return friends

@api_view(['POST'])
def coffe_friends(request):
    # print("request:  ", request)
    check = False
    if request.method == 'POST':
        data = request.data
        for key in data:
            # print(key)
            if key == "coffee_selected":
                # print("key", key, data[key])
                friends = next_to_friends(data[key])
                # print(friends)
                for friend in friends:
                    check  = True
                    # print("friend", friend, type(friend))
                if check == False:
                    friends = ["Be the First!"]      
            else:
                friends = ["The request key invalid"]

    return Response(friends, status=status.HTTP_200_OK)




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

    def get_post_response_data(self, request, token, instance):
        # print('instance', instance.user.id)
        UserSerializer = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
            'user_pk': instance.user.id,
            'is_staff': instance.user.staff
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
            # print('request.user',request.user)
        return data

    def post(self, request, format=None):
        serializer = MyAuthTokenSerializer(data=request.data)
        # print('serializer: ', serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
# https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
# https://james1345.github.io/django-rest-knox/

@api_view(['POST'])
def logins(request):
    if request.method == 'POST':
        data = request.data
        serializer = LoginSerializer(data=data)
        # data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Succesfully login"
            data['email'] = account.email
            data['password'] = account.password
        else:
            data = serializer.error        
        return Response(data, status=status.HTTP_200_OK)

# Learning objects:
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_tasks(request):
    tasks = Task.objects.all()
    # print(tasks)
    serializer = TaskSerializer(tasks, many=True)
    # print('GET: ',serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def create_task(request):
    data = request.data
    # print('POST: ', data)
    serializer = TaskSerializer(data=data)
    # print('serializer: ', serializer)
    if serializer.is_valid():
        ser_data = serializer.data
        # print('VALID ser_data',ser_data)
        # Task.objects.create(name=ser_data['name'])
        Task.objects.create(
            name = ser_data['name'], 
            age = ser_data['age'])        
        return Response(serializer.data, status=status.HTTP_200_OK)