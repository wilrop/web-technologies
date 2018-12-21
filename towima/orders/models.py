from django.db import models
from products.models import Product
from pharmacies.models import Pharmacy
from django.contrib.auth.models import User
from pharmacies.models import Stock

class Other(models.Model):
    DEFAULT_PK=1
    name=models.CharField(max_length=1024)

# Definition of the model to save and order in the database. An order is placed by a customer and can be deleted by the user or pharmacist
# and be filled by the pharmacist if it is ready. The order constains the user that placed the order, the first name, the last name, the email
# the address, the product, the pharmacy, the price of the product, the quantity, the total price, field if the order is filled and dates 
# When the orders are created and updated. This model also contains a custom save function to calculate the total price and a function to get the price.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=Other.DEFAULT_PK)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    quantity = models.PositiveIntegerField(default=1)
    filled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        stock_ = Stock.objects.get(product=self.product, pharmacy=self.pharmacy)
        self.unit_price = stock_.product_price
        self.total_price = self.unit_price * self.quantity
        super(Order, self).save(*args, **kwargs)
    