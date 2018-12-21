from django.db import models
from django.urls import reverse
from products.models import Product
from django.contrib.auth.models import User
from django.utils import timezone

class Other(models.Model):
    DEFAULT_PK=1
    name=models.CharField(max_length=1024)

# Definition of the Pharmacy model. A pharmacy is created by a pharmacist.
class Pharmacy(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, default=Other.DEFAULT_PK)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    address = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(default='example@example.com')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product, through='Stock', related_name="products+")
    pharmacists = models.ManyToManyField(User, through='Employee', related_name="pharmacists+")

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('pharmacies:pharmacy', args=[self.pk])

# definition of a model to create a relation between a pharmacy and a pharmacist. This is usefull to add employees to the pharmacy.
# The relation contains the salary of the employee.
class Employee(models.Model):
    pharmacist = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    salary= models.PositiveIntegerField(default=0)

# Definition of a model to create a relation between a product and a pharmacy. A pharmacy can have multiple products and a product can be
# present in multiple pharmacies. The relation contains a price and an amount.
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    product_stock = models.PositiveIntegerField(default=0)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Comments(models.Model):
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_user')
    pharmacy = models.ForeignKey('Pharmacy', on_delete=models.CASCADE, related_name='rated_user')
    rating = models.IntegerField()