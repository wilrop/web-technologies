from django import forms
from pharmacies.models import Pharmacy

class PharmacyForm(forms.ModelForm):
    name = forms.CharField(max_length = 70)
    phone_number = forms.CharField(max_length=12)
    address = forms.CharField(max_length = 50)
    
    
    class Meta:
        model = Pharmacy
        fields = ('name','address','phone_number')
        widgets = {'slug': forms.HiddenInput()}