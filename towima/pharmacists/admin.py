from django.contrib import admin
<<<<<<< HEAD
from pharmacists.models import Pharmacy, Comments, Rating

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address']
    list_filter = ['name']
    list_editable = ['phone_number', 'address']
admin.site.register(Pharmacy, PharmacyAdmin)
=======
from pharmacists.models import Comments
>>>>>>> 9b582bd3a4eebe85db60551cf86a0ba3c43e532c

admin.site.register(Comments)
admin.site.register(Rating)
