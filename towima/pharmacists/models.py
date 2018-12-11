from django.db import models
from django.utils import timezone

# Create your models here.
class Pharmacy(models.Model):
    name = models.CharField(max_length = 70)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length = 50)

class Comments(models.Model):
    pharmacist = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Rating(models.Model):
    user = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='rating_user')
    pharmacist = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='rated_user')
    rating = models.IntegerField()

