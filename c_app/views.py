from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# knox token auth
from rest_framework import generics, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# from .serializers import UserSerializer, RegisterSerializer
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