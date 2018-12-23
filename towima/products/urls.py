from django.urls import path
from django.conf.urls import url
from products import views

app_name = 'products'
urlpatterns = [
    path('list/', views.products_list, name='list'),                                                # URL to display al the products in the database
    #path('add/', views.add_product, name='add_product'),                                           # URL to add a product to the database (not used right now)
    url(r'^(?P<product_id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail')    # URL to see a specific product page.
]