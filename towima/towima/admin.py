from django.contrib import admin
from towima.models import Profile, Category, Product

# Register the Profile model in the admin page.
admin.site.register(Profile)

class CategoryAdmin(admin.ModelAdmin):
    # Set list_display to control which fields are displayed on the change list page of the admin.
    # If you don’t set list_display, the admin site will display a single column that displays the __str__() representation of each object.
    list_display = ['name', 'slug']
    
    # Set prepopulated_fields to a dictionary mapping field names to the fields it should prepopulate from
    # When set, the given fields will use a bit of JavaScript to populate from the fields assigned. 
    # The main use for this functionality is to automatically generate the value for SlugField fields from one or more other fields.
    # Fields are prepopulated on add forms but not on change forms. 
    # It’s usually undesired that slugs change after an object is created (which would cause an object’s URL to change if the slug is used in it).
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    
    # Set list_filter to activate filters in the right sidebar of the change list page of the admin.
    list_filter = ['available', 'created', 'updated', 'category']

    # Set list_editable to a list of field names on the model which will allow editing on the change list page. 
    # That is, fields listed in list_editable will be displayed as form widgets on the change list page, allowing users to edit and save multiple rows at once.
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

# A lot of information in the comments comes from the documentation.