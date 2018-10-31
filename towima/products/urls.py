from django.urls import path
from django.conf.urls import url
from products import views

urlpatterns = [
    path('list/', views.products_list, name='list'),
]