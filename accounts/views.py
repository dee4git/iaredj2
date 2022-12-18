from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

import iaredj.context_processor
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # if the user logs in for a purpose the user should automatically be redirected to that page
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == "POST" or "GET":
        logout(request)
        # iaredj.context_processor.is_staff(request)
        return redirect('home')

#
# def profile(request):
#     return render(request, "profile.html")
