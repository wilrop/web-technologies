from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from pharmacies.models import Pharmacy

class Other(models.Model):
    DEFAULT_PK=1
    name=models.CharField(max_length=1024)

# Create a user profile model. This model will have a OneToOne with User and some extra profile attributes.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default=0000000000)
    date_of_birth = models.DateField()
    address = models.CharField(max_length = 50)
    user_type = models.CharField(max_length=126, default='Customer')
    verified = models.BooleanField(default=False)

# Create a Cart model. Every user on the website will have a Cart. This cart is used for placing orders on the website.
# The cart contains products with a through model called Item. An Item is a product that is in the Cart. It contains the name of the product
# the name of the pharmacy, the quantity and the unit price of the product.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Item', related_name="items+")

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=Other.DEFAULT_PK)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)