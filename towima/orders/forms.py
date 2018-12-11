from django import forms
from .models import Order
from products.models import Product
from pharmacies.models import Pharmacy

class OrderForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label='E-Mail')
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    pharmacy = forms.ModelChoiceField(queryset=Pharmacy.objects.all())
    address = forms.CharField()
    postal_code = forms.CharField()
    city = forms.CharField()
    quantity = forms.IntegerField()

    class Meta:
        model = Order
        fields = (              # The order of the fields.
            'first_name', 
            'last_name', 
            'email',
            'address',
            'city',
            'postal_code',
            'product',
            'pharmacy',
            'quantity',
        ) 

  