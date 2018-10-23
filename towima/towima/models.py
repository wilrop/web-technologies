from django.db import models
from django.contrib.auth.models import User

# Create a user profile model. This model will have a OneToOne with User and some extra profile attributes.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    date_of_birth = models.DateField()
    address = models.CharField(max_length = 50)

# Definition of the model Category. This class is used to categorise the different products to get a good overview of the products.
# The used attributes are name for the name of the Category and the slug for the URl.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        # The ordering for the object, for use when obtaining lists of objects:
        ordering = ('name',)
        
        # A human-readable name for the object, singular.
        # If this isn’t given, Django will use a munged version of the class name: CamelCase becomes camel case.
        verbose_name = 'category'
        
        # A human-readable name for the object, plural
        verbose_name_plural = 'categories'

    # A Python method that returns a string representation of the object. 
    # This is what Django will use whenever a model instance needs to be coerced and displayed as a plain string. 
    # Most notably, this happens when you display an object in an interactive console or in the admin.
    # You’ll always want to define this method; the default isn’t very helpful at all.
    def __str__(self):
        return self.name
    
    # This tells Django how to calculate the URL for an object. Django uses this in its admin interface, and any time it needs to figure out a URL for an object.
    # Any object that has a URL that uniquely identifies it should define this method.
    # (From documentation)
    def get_absolute_url(self):
        return reverse('towima:product_list_by_category', args=[self.slug])


# Definition of the model Product. This class is used to put the different products in the database.
# The used attributes are catergory for the used Category, name for the name of the product,
# slug for the URl, image for a product image, description for a product description.
# price for the price of the product, stock for the amount that is still left for the product,
# available to see if a product is still available(You can use this to make products offline),
# created for the date when the product is created in the database.
# updated for the date when the product is last updated in the database.
class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    #pip install pillow to get this feature
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True) 
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),) 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
       return reverse('towmima:product_detail', args[self.id, self.slug])


# A lot of information in the comments comes from the documentation.