from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from accounts.forms import SignUpForm, EditProfileForm
from django.core.mail import send_mail
from accounts.models import Profile
from authy.api import AuthyApiClient
from .forms import TokenForm, VerificationForm
from orders.models import Order

authy_api = AuthyApiClient('jqr27nutYbPgCmIilN0ByqTTe1xBu6Wp')


# Define a signup view. This will provide the user with a signup page and the correct functionality.
def signup(request):
    template = 'accounts/signup.html'

    if request.method == 'POST':                # When we POST the form.
        form = SignUpForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            request.session['username'] = form.cleaned_data['username']
            '''request.session['phone_number'] = form.cleaned_data['phone_number'][1:]
            request.session['country_code'] = 32
            authy_api.phones.verification_start(
                phone_number=form.cleaned_data['phone_number'][1:], # Drop the zero
                country_code=32,                                     # Only Belgium
                via='sms'
            )'''
            return redirect('phone_verification')
    else:                                       # When we GET the form.
        form = SignUpForm()                     # Provide the form to the user.
    return render(request, template, {'form': form})

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            request.session['country_code'] = form.cleaned_data['country_code']
            authy_api.phones.verification_start(
                form.cleaned_data['phone_number'],
                form.cleaned_data['country_code'],
                via='sms'
            )
            return redirect('verify')
    else:
        form = VerificationForm()
    return render(request, 'accounts/phone_verification.html', {'form': form})

# Verify the phonenumber
def verify(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            verification = authy_api.phones.verification_check(
                request.session['phone_number'],
                request.session['country_code'],
                form.cleaned_data['token']
            )
            if verification.ok():
                user = User.objects.get(username=request.session['username'])
                profile = Profile.objects.get(user=user)
                profile.phone_number = request.session['phone_number']
                profile.verified = True
                send_mail('Welcome to PharmaTowi', 'Welcome to our website, Your account has been verified!', 'pharmatowi@gmail.com', [getattr(user, 'email')], fail_silently=False,)
                profile.save()
                return redirect('login')
            else:
                for error_msg in verification.errors().values():
                    form.add_error(None, error_msg)
    else:
        form = TokenForm()
    return render(request, 'accounts/token_validation.html', {'form': form})

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

def login_view(request):
    template = 'accounts/login.html'

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)  # Use the preexisting PasswordChangeForm.

        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            profile = Profile.objects.get(user=user)
            request.session['username'] = form.cleaned_data.get('username')
            if profile.verified:
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')

            else:
                return redirect('phone_verification')

    else:
        form = AuthenticationForm() 

    return render(request, template, {'form': form})

def edit_home(request):
    template ='accounts/edit_home.html'
    context={}
    return render(request, template, context)

def orders(request):
    template = 'accounts/orders.html'
    user = request.user
    orders = Order.objects.filter(user=user)
    args = {'user': user, 'orders':orders}   
    return render(request, template, args)

