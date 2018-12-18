from django.urls import path
from django.conf.urls import url
from pharmacies import views

app_name = 'pharmacies'
urlpatterns = [
    path('create_pharma/', views.create_pharma, name='create_pharma'),
    path('search/', views.search, name='search'),
    url(r'^pharmacy/(?P<pk>\d+)/$', views.pharmacy, name='pharmacy'),
    path('find_pharma/', views.find_pharma, name='findpharma'),
    path('add_comment_to_pharmacy/', views.add_comment_to_pharmacy, name='add_comment_to_pharmacy'),
    path('add_rating_to_pharmacy/', views.add_rating_to_pharmacy, name='add_rating_to_pharmacy'),
    path('product_detail/<pk>/<ppk>', views.product_detail, name='product_detail'),
    path('get_locations/', views.get_locations, name='get_locations'),
    path('pharma_settings/', views.pharma_settings, name='pharma_settings'),
    path('orders/', views.pharmacy_orders, name='orders'),
    path('order_delete/<pk>', views.order_delete, name='order_delete'),
    path('confirm_order/<pk>', views.confirm_order, name='confirm_order'),
    path('add_product/', views.add_product, name='add_product'),
]