from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import SignUpForm, EditProfileForm

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

# When a user wants to view his/her own profile.
def profile(request):
    template = 'accounts/profile.html'
    args = {'user': request.user}   
    return render(request, template, args)

# When a user wants to edit his/her profile.
def edit_profile(request):
    template = 'accounts/edit_profile.html'

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, template, {'form': form})

# When a user wants to change their password.
def change_password(request):
    template = 'accounts/change_password.html'

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)  # Use the preexisting PasswordChangeForm.

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # Because the user changed their password, we need to update the session.
            return redirect('home')

    else:
        form = PasswordChangeForm(user=request.user) 
    return render(request, template, {'form': form})

