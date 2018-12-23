from django import forms
from .models import Product, Category 
from accounts.models import Cart, Item
from pharmacies.models import Pharmacy
from products.models import Product
from django.contrib.auth.models import User

# Definition of the Form to add a Product to the database. This currently not used in our website but it could be used in the future.
class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField()
    image = forms.ImageField(required=False)
    description = forms.CharField()
    available = forms.BooleanField()

    class Meta:
        model = Product
        fields = (             
            'category', 
            'name', 
            'image',
            'description',
            'available',
        )

# Definiton of the form displayed on the product page of a product to add a certain quantity of the product to the cart of the
# currently logged in user.
class AddtoCartForm(forms.ModelForm):
    pharmacy = forms.ModelChoiceField(queryset=Pharmacy.objects.all())
    quantity = forms.IntegerField()

    class Meta:
        model = Item
        fields = (              # The order of the fields.
            'pharmacy',
            'quantity',
        )