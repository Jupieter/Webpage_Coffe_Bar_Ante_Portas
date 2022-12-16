from django.shortcuts import render, redirect, get_object_or_404, redirect 
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterForm, LoginForm
from .models import User
# from django.utils.http import is_safe_url
from django.contrib import messages
# token generator
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from knox.models import AuthToken

User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        new_user = User.objects.create_user(email, username, password, first_name, last_name)
        if new_user is not None:
            messages.success(request, "Created User.")
            return redirect('accounts:login')
        
        messages.warning(request, "Create Error !")


    context = {
        "form": form
    }

    return render(request, "accounts/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_url')
    form = LoginForm(request.POST or None)
    context = { "form": form }

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        print("USER:    ", user)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        else:
            messages.warning(request, 'Credentials error.')    
    return render(request, "accounts/login.html", context)

def token_gen(request):
    adat1 = []
    adat2 = []
    for user in User.objects.all():
        AuthToken.objects.create(user=user)[1]
        token = AuthToken.objects.filter(user=user)
        adat1.append(user)
        adat2.append(token)
        print(user, '---',token) 
    context = {'adat1':adat1, 'adat2':adat2} 
    return render(request, "accounts/token.html", context)    
    
