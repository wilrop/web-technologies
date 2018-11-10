from django.urls import path
from django.conf.urls import url
from products import views

app_name = 'products'
urlpatterns = [
    path('list/', views.products_list, name='list'),
    url(r'^(?P<product_id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail')
]