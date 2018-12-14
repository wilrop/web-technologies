from products.models import Product, Category
from django.contrib.auth.models import User
from pharmacies.models import Comments, Rating, Pharmacy
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('category', 'name', 'description',)

class PharmacySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ('name', 'address', 'phone_number', 'email',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)

class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    class Meta:
        model = Comments
        fields = ('pharmacy', 'text', 'author', 'created_date',)

class RatingSerializer(serializers.HyperlinkedModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ('pharmacy', 'user','rating',)




        