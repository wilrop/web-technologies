from django.db import models

# Create your models here.
class Pharmacy(models.Model):
    name = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length = 50)
