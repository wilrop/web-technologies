from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from accounts.forms import SignUpForm, EditProfileForm
from django.core.mail import send_mail
from accounts.models import Profile, Cart, Item
from authy.api import AuthyApiClient
from .forms import TokenForm, VerificationForm
from orders.models import Order
from twilio.rest import Client
from pharmacies.models import Pharmacy

authy_api = AuthyApiClient('jqr27nutYbPgCmIilN0ByqTTe1xBu6Wp')


# Define a signup view. This will provide the user with a signup page and the correct functionality.
def signup(request):
    template = 'accounts/signup.html'

    if request.method == 'POST':                # When we POST the form.
        form = SignUpForm(request.POST)
        if form.is_valid():                     # Check if the form is valid.
            form.save()
            request.session['username'] = form.cleaned_data['username']
            if form.cleaned_data['user_type'] == "Pharmacist":
                return redirect('pharmacies:create_pharma')
            else:
                return redirect('phone_verification')
    else:                                       # When we GET the form.
        form = SignUpForm()                     # Provide the form to the user.
    return render(request, template, {'form': form})

# This view will check if a username is already taken or not and respond with JSON code.
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

# This view will let the user input their phone number for the phone verification process.
def phone_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.session['phone_number'] = form.cleaned_data['phone_number']
            request.session['country_code'] = form.cleaned_data['country_code']
            authy_api.phones.verification_start(  # Send a SMS to the user with their code through the API.
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
            verification = authy_api.phones.verification_check( # Check the verification code throught the API.
                request.session['phone_number'],
                request.session['country_code'],
                form.cleaned_data['token']
            )
            if verification.ok():
                user = User.objects.get(username=request.session['username'])
                profile = Profile.objects.get(user=user)
                profile.phone_number = request.session['phone_number']
                profile.verified = True # Set the verified field in the profile model to true, because the user has been verified.

                # Send an email.
                send_mail('Welcome to PharmaTowi', 'Welcome to our website, Your account has been verified!', 'pharmatowi@gmail.com', [getattr(user, 'email')], fail_silently=False,)
                profile.save()
                cart = Cart.objects.create(user=user) # Create a cart for the user.
                cart.save()
                return redirect('login')
            else: # If verification was not successful, add an error.
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

# The login view that will be requested whenever a user tries to log in on our website.
def login_view(request):
    template = 'accounts/login.html'

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)  # Use the preexisting PasswordChangeForm.

        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data['username'])
            profile = Profile.objects.get(user=user) # Get the frofile from the user.
            request.session['username'] = form.cleaned_data.get('username')
            if profile.verified: # If the profile is verified, let the user log in.
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')

            else: # If not, redirect to phone verification.
                return redirect('phone_verification')

    else:
        form = AuthenticationForm() 

    return render(request, template, {'form': form})

def edit_home(request):
    template ='accounts/edit_home.html'
    context={}
    return render(request, template, context)

# Define a order view. This is a view that is used for displaying the orders of the user. There are 2 types of orders, open orders
# and filled orders. Open orders are orders that are not filled by the pharmacy and filled orders are orders that are filled by the pharmacy.
def orders(request):
    template = 'accounts/orders.html'
    user = request.user
    orders = Order.objects.filter(user=user)
    args = {'user': user, 'orders':orders}   
    return render(request, template, args)

# Define a cart view. This is a view that is used for displaying the cart of the user. This view also calculates the total price
# of the items that are present in the cart.
def cart(request):
    template = 'accounts/cart.html'
    user = request.user
    cart = Cart.objects.get(user=user)
    items = Item.objects.filter(cart=cart)

    total_price = 0
    for item in items:
        total_price += item.unit_price * item.quantity
    args = {'user': user, 'items': items, 'total_price': total_price}   
    return render(request, template, args)

# Define an item delete view. This is a view that is used to remove an item (product) from the cart of the customer.
def item_delete(request, pk):
    item = Item.objects.get(pk=pk) 
    item.delete()
    return redirect(request.META['HTTP_REFERER'])

# Define an order delete view. This is a view that is used for the delete button in the customer his orders. The customer can only delete
# orders that are not filled by the pharmacy.
def order_delete(request, pk):
    order = Order.objects.get(pk=pk) 
    order.delete()
    return redirect(request.META['HTTP_REFERER'])

# Define a place order view. This view will remove all the items (products) from the user his cart and it it will change the items
# into orders. These orders will be displayed in the order page of the user and the order page of the pharmacy. An email will also
# be send to the pharmacy to inform the pharmacy that a user has placed an order.
def place_orders(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cart = Cart.objects.get(user=user)
    items = Item.objects.filter(cart=cart)
    for item in items:
        Order.objects.bulk_create([Order(user=user, first_name=user.first_name, last_name=user.last_name, email=user.email, address=profile.address, product=item.product, pharmacy=item.pharmacy, quantity=item.quantity)])
        send_mail('New Order', 'You have a new order from a customer!', 'pharmatowi@gmail.com', [getattr(item.pharmacy, 'email')], fail_silently=False,)
        item.delete()
    all_orders = Order.objects.all()
    for order in all_orders:
        order.save()
    return redirect(request.META['HTTP_REFERER'])