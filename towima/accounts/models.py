from django.db import models
from django.contrib.auth.models import User

# Create a user profile model. This model will have a OneToOne with User and some extra profile attributes.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default=0000000000)
    date_of_birth = models.DateField()
    address = models.CharField(max_length = 50)
    user_type = models.CharField(max_length=126, default='Customer')
    verified = models.BooleanField(default=False)
