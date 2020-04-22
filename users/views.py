import json
import urllib
import urllib.request
from django.http import *


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.conf import settings		  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result ['success']:
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'You Account Has Been Created! Have Fun! {username}!')
                return redirect('login')
            else:
                messages.error(request, f'Invalid Data. Please Try Again!')
                return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':    
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
                 #''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
                   #''' End reCAPTCHA validation '''
            if result ['success']:
                u_form.save()
                p_form.save()
                messages.success(request, f'You Account Has Been Updated! cool!')
                return redirect('profile')
            else:
                messages.error(request, f'Invalid Captcha, Please prove that you are human!')
                return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
	'u_form': u_form,
	'p_form' : p_form
    }
    return render(request, 'users/profile.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/users/logout.html')
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            #''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
                   #''' End reCAPTCHA validation '''
            if result ['success']:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
            else:
                messages.error(request, f'Invalid Captcha, Please prove that you are human!')
                return redirect('profile')

            if user is not None:
                 print(user)
                 login(request, form.get_user())
                 return HttpResponseRedirect('/')
            else:
                print('User not found')
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'users/login.html', {'form': form})
