from django.conf import settings
from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadProfilePhotoForm
from .models import UserProfile


@login_required
def upload_profile_photo(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UploadProfilePhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # redirige vers la page profil
    else:
        form = UploadProfilePhotoForm(instance=profile)
    return render(request, 'authentication/upload_profile_photo.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'authentication/profile.html')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    message = ''
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form)
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
        if user is not None:
                login(request, user)
                return redirect('home')
        else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})
