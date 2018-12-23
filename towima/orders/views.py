from django.shortcuts import render, redirect
from pharmacies.models import Pharmacy
from .forms import OrderForm
from twilio.rest import Client

# View that is created for making a seperate order. There is also sms notification for the order to the pharmacy.
# This is currently not used in our website but is nog removed because it could be used in the furure if needed.
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            product = form.cleaned_data.get('product')
            pharmacy = form.cleaned_data.get('pharmacy')
            address = form.cleaned_data.get('address')

            pharmacy_object = Pharmacy.objects.get(name=pharmacy)
            phone_number = pharmacy_object.phone_number
            print(phone_number)
            # Your Account SID from twilio.com/console
            account_sid = "ACb651004e985e1af070bb32fa81344449"
            # Your Auth Token from twilio.com/console
            auth_token  = "77ac7d6c5d77ea10284e2a61898aca64"

            client = Client(account_sid, auth_token)

            message = client.messages.create(
                to=phone_number, 
                from_="+32460201263",
                body="You have a new order!")

            return redirect('home')
    else:                                       
        form = OrderForm()
    form = OrderForm()
    return render(request, 'orders/order.html', {'form': form})