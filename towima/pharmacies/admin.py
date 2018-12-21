from django.contrib import admin
from pharmacies.models import Pharmacy, Stock, Employee, Comments, Rating

# Register the Pharmacy model in the admin page.
admin.site.register(Pharmacy)

# Register the Comments model in the admin page.
admin.site.register(Comments)

# Register the Rating model in the admin page.
admin.site.register(Rating)

# Register the Stock model in the admin page.
admin.site.register(Stock)

# Register the Employee model in the admin page.
admin.site.register(Employee)