from products.models import Product, Category
from django.contrib.auth.models import User
from pharmacies.models import Comments, Rating, Pharmacy
from rest_framework import serializers

# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes 
# that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, 
# allowing parsed data to be converted back into complex types, after first validating the incoming data.
# source: https://www.django-rest-framework.org/api-guide/serializers/

# Definition of the serializer of the Category. Only the name is given.
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

# Definition of the serializer of the Product. Only the name, category and description is given.
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('category', 'name', 'description',)

# Definition of the serializer of the Pharmacy. Only the name, address, phone number and email is given.
class PharmacySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ('name', 'address', 'phone_number', 'email',)

# Definition of the serializer of the Users. Only the user name, first name and last name is given.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)

# Definition of the serializer of the Comments. Only the pharmacy, text, author and date of creation is given.
class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    class Meta:
        model = Comments
        fields = ('pharmacy', 'text', 'author', 'created_date',)

# Definition of the serializer of the Ratin. Only the pharmacy, the user and the rating is given.
class RatingSerializer(serializers.HyperlinkedModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ('pharmacy', 'user','rating',)




        