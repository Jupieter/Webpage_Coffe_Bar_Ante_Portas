from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login

from django.contrib import messages

User = get_user_model()


def register_page(request):
    return render(request, "accounts/register.html")


def login_page(request):
    return render(request, "accounts/login.html")


def guest_register_view(request):
   return render(request, "accounts/login.html")
