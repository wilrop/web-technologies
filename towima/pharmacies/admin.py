from django.contrib import admin
from pharmacies.models import Pharmacy, Stock, Employee, Comments, Rating

admin.site.register(Pharmacy)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Stock)
admin.site.register(Employee)