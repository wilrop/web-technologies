from django import forms
from .models import Order
from products.models import Product
from pharmacies.models import Pharmacy
from django.forms import formset_factory, BaseFormSet

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

class TestForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    pharmacy = forms.ModelChoiceField(queryset=Pharmacy.objects.all())
    quantity = forms.IntegerField()

    class Meta:
        model = Order
        fields = (              # The order of the fields.
            'product', 
            'pharmacy', 
            'quantity',
        )

class BaseTestFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["my_field"] = forms.CharField()

TestFormSet = formset_factory(TestForm)