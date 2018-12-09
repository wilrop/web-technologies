from django.db import models
from products.models import Product
from pharmacies.models import Pharmacy

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_price(self):
        return self.price * self.quantity
    