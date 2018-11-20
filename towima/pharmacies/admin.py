from django.contrib import admin
from pharmacies.models import Pharmacy, Stock

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'address', 'phone_number']
    list_filter = ['name']
    list_editable = ['address', 'phone_number']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Pharmacy, PharmacyAdmin)


admin.site.register(Stock)