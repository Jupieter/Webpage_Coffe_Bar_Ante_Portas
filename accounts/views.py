from django.shortcuts import render, redirect, get_object_or_404, redirect 
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterForm, LoginForm
from .models import User
# from django.utils.http import is_safe_url
from django.contrib import messages
# token generator
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        new_user = User.objects.create_user(email, password, first_name, last_name)
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

    
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    adat = 'Üres'
    form = LoginForm(request.POST or None)
    context = { "form": form }

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        user_list = get_object_or_404(User, email=email)       
        first_name = user_list.first_name
        if user is not None:
            adat = first_name
            # render(request, "accounts/login.html",{"form": form, 'adat': adat} )
            login(request, user)
            return redirect('home_url')
            try:
                del request.session['guest_email_id']
            except:
                pass

        else:
            # adat = ['invalid', email, password, user, first_name]
            # render(request, "accounts/login.html", {"form": form, 'adat': adat})
            messages.warning(request, 'Credentials error.')

    
    return render(request, "accounts/login.html", {"form": form, 'adat': adat})

def token_gen(request):
    adat1 = []
    adat2 = []
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
        token = Token.objects.filter(user=user)
        print(user, token) 
        adat1.append(user)
        adat2.append(token)
    context = {'adat1':adat1, 'adat2':adat2} 
    return render(request, "accounts/token.html", context)    
    
