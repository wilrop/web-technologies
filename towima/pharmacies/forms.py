from django import forms
from pharmacies.models import Pharmacy, Comments, Stock
from products.models import Product
from accounts.models import Item
from django.contrib.auth.models import User

# Definition of the form the create a pharmacy. A pharmacy is created when a pharmacist does a sign up on the website. This also contains a
# custom save funtion for the Pharmacy to save the owner of the pharmacy (the currenlty logged in user).
class PharmacyForm(forms.ModelForm):
    name = forms.CharField(max_length = 70)
    email = forms.CharField(max_length = 50)
    phone_number = forms.CharField(max_length=12)
    address = forms.CharField(max_length = 50)
    
    
    class Meta:
        model = Pharmacy
        fields = ('name','address', 'email', 'phone_number')
        widgets = {'slug': forms.HiddenInput()}

    def save(self, user, commit = True):
        user_id = User.objects.get(username=user)
        name = self.cleaned_data['name']
        phone_number = self.cleaned_data['phone_number']
        address = self.cleaned_data['address']
        email = self.cleaned_data['email']
        if commit:         
            pharmacy = Pharmacy(owner=user_id, name=name, address=address, phone_number=phone_number, email=email)
            pharmacy.save()
            
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def save(self, pk, user, commit = True):
        comment = super().save(commit=False)
        pharmacy = Pharmacy.objects.get(pk = pk)
        comment.pharmacy = pharmacy
        comment.author = user

        if commit:
            comment.save()
        return comment

class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField()

    class Meta:
        model = Item
        fields = (              # The order of the fields.
            'quantity',
        )

# Definition of the form to add stock and price of a certain product in the database to the pharmacy. The pharmacist needs to select
# a product and choose the amount in Stock and the price of the product in the pharmacy. This also contains a custom save function so there
# is only one relation between a product and a pharmcy, otherwise the current relation needs to be removed or modified.
class AddStockForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    stock = forms.IntegerField()
    price = forms.DecimalField()

    class Meta:
        model = Stock
        fields = (              # The order of the fields.
            'product',
            'stock',
            'price',
        )
    def save(self, pharmacy, commit = True):
        product = self.cleaned_data['product']
        stock = self.cleaned_data['stock']
        price = self.cleaned_data['price']
        if commit:
            if not Stock.objects.filter(pharmacy=pharmacy, product=product):
                stock = Stock(product=product, pharmacy=pharmacy, product_stock=stock, product_price=price)
                stock.save()