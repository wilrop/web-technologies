from django.urls import path
from django.conf.urls import url
from orders import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.create_order, name='create'),
    path('test/', views.test_order, name='test'),
]