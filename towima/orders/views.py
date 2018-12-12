from django.shortcuts import render, redirect
from pharmacies.models import Pharmacy
from .forms import OrderForm
from twilio.rest import Client

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            product = form.cleaned_data.get('product')
            pharmacy = form.cleaned_data.get('pharmacy')
            address = form.cleaned_data.get('address')
            postal_code = form.cleaned_data.get('postal_code')
            city = form.cleaned_data.get('city')

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