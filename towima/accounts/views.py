from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

# Define a signup view. This will provide the user with a signup page and the correct functionality.
def signup(request):
    template = 'accounts/signup.html'

    if request.method == 'POST':                # When we POST the form.
        form = SignUpForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')         
    else:                                       # When we GET the form.
        form = SignUpForm()                     # Provide the form to the user.
    return render(request, template, {'form': form})

def profile(request):
    template = 'accounts/profile.html'
    args = {'user': request.user}   
    return render(request, template, args)

def edit_profile(request):
    template = 'accounts/edit_profile.html'

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, template, {'form': form})

def change_password(request):
    template = 'accounts/change_password.html'

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')

    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request, template, {'form': form})

