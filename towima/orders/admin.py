from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
admin.site.register(Order, OrderAdmin)