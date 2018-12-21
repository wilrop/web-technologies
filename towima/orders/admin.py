from django.contrib import admin
from .models import Order

# Register the Order model in the admin page. There is also a custom save function defined to save the current user.
class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
admin.site.register(Order, OrderAdmin)