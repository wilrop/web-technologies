from django.shortcuts import render, redirect
from .forms import OrderForm
# Create your views here.

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
            return redirect('home')
    else:                                       
        form = OrderForm()
    form = OrderForm()
    return render(request, 'orders/order.html', {'form': form})