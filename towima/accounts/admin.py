from django.contrib import admin
from accounts.models import Profile, Cart, Item

# Register the Profile model in the admin page.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Item)
