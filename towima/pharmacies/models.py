from django.db import models
from django.urls import reverse
from products.models import Product
from django.contrib.auth.models import User
from django.utils import timezone

class Pharmacy(models.Model):
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

class Employee(models.Model):
    pharmacist = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    salary= models.PositiveIntegerField(default=0)

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