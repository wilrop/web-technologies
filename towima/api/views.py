from django.shortcuts import render
from django.contrib.auth.models import User
from products.models import Product, Category
from pharmacies.models import Comments, Rating, Pharmacy
from rest_framework import viewsets
from api.serializers import ProductSerializer, CategorySerializer, CommentsSerializer, RatingSerializer, PharmacySerializer, UserSerializer

# Definition of a view to display all the products with the correct serializer in the API page.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get']

# Definition of a view to display all the product categories with the correct serializer in the API page.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get']

# Definition of a view to display all the comments on a pharmacy with the correct serializer in the API page.
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    http_method_names = ['get']

# Definition of a view to display all the ratings on a pharmacy with the correct serializer in the API page.
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    http_method_names = ['get']

# Definition of a view to display all the pharmacies with the correct serializer in the API page.
class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    http_method_names = ['get']

# Definition of a view to display all the users with the correct serializer in the API page.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']