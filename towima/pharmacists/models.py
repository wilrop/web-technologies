from django.db import models
from django.utils import timezone

class Comments(models.Model):
    pharmacist = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
