from django.contrib import admin
from pharmacists.models import Pharmacy, Comments

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address']
    list_filter = ['name']
    list_editable = ['phone_number', 'address']
admin.site.register(Pharmacy, PharmacyAdmin)

admin.site.register(Comments)
