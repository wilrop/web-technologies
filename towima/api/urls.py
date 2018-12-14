from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='Products')
router.register(r'categories', views.CategoryViewSet, basename='Categories')
router.register(r'comments', views.CommentsViewSet, basename='Comments')
router.register(r'ratings', views.RatingViewSet, basename='Ratings')
router.register(r'pharmacies', views.PharmacyViewSet, basename='Pharmacies')
router.register(r'users', views.UserViewSet, basename='Users')

app_name = 'api'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]