from django.contrib import admin
from accounts.models import Profile, Cart, Item

# Register the Profile model in the admin page.
admin.site.register(Profile)

# Register the Cart model in the admin page.
admin.site.register(Cart)

# Register the Item model in the admin page.
admin.site.register(Item)
