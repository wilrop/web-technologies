from django import forms
from .models import Product, Category

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