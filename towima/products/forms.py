from django import forms
from .models import Product, Category 
from accounts.models import Cart, Item
from pharmacies.models import Pharmacy
from products.models import Product
from django.contrib.auth.models import User

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

class AddtoCartForm(forms.ModelForm):
    pharmacy = forms.ModelChoiceField(queryset=Pharmacy.objects.all())
    quantity = forms.IntegerField()

    class Meta:
        model = Item
        fields = (              # The order of the fields.
            'pharmacy',
            'quantity',
        )