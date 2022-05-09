from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import LoginForm
from django.contrib import messages

User = get_user_model()


def register_page(request):
    return render(request, "accounts/register.html")


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_url')
    
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    adat = next_post

    form = LoginForm(request.POST or None)
    context = {"form": form, 'adat': adat}

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        user = authenticate(request, username=username, email=email, password=password)
        # user = authenticate(request, email=email, password=password)
        if user is not None:
            # login(request, user)
            adat = ['valid', username, email, password, user] 
            render(request, "accounts/login.html",{"form": form, 'adat': adat} )

        else:
            adat = ['invalid', username, email, password, user]
            render(request, "accounts/login.html", {"form": form, 'adat': adat})

            # messages.warning(request, 'Belépési hiba')
    

    return render(request, "accounts/login.html", {"form": form, 'adat': adat} )


def guest_register_view(request):
   return render(request, "accounts/login.html")
