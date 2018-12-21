from django import forms
from .models import Order
from products.models import Product
from pharmacies.models import Pharmacy

 # Form to create a seperate order in the database. This is currently not used in our website, but not removed because it
 # is something that could be used on a later date.
class OrderForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label='E-Mail')
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    pharmacy = forms.ModelChoiceField(queryset=Pharmacy.objects.all())
    address = forms.CharField()
    quantity = forms.IntegerField()

    class Meta:
        model = Order
        fields = (              # The order of the fields.
            'first_name', 
            'last_name', 
            'email',
            'address',
            'product',
            'pharmacy',
            'quantity',
        )