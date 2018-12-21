from django.urls import path
from django.conf.urls import url
from pharmacies import views

app_name = 'pharmacies'
urlpatterns = [
    path('create_pharma/', views.create_pharma, name='create_pharma'),                                  # URL to create a pharmacy
    path('search/', views.search, name='search'),                                                       # URL to search a pharmacy
    url(r'^pharmacy/(?P<pk>\d+)/$', views.pharmacy, name='pharmacy'),                                   # URL to a pharmacy
    path('find_pharma/', views.find_pharma, name='findpharma'),                                         # URL to find a pharmacy
    path('add_comment_to_pharmacy/', views.add_comment_to_pharmacy, name='add_comment_to_pharmacy'),    # URL to add a comment to a pharmacy
    path('add_rating_to_pharmacy/', views.add_rating_to_pharmacy, name='add_rating_to_pharmacy'),       # URL to add a rating to  a pharmacy
    path('product_detail/<pk>/<ppk>', views.product_detail, name='product_detail'),                     # URL to see a product of a pharmacy
    path('get_locations/', views.get_locations, name='get_locations'),                                  # URL to the location of a pharmacy
    path('pharma_settings/', views.pharma_settings, name='pharma_settings'),                            # URL to see the settings of a pharmacy
    path('orders/', views.pharmacy_orders, name='orders'),                                              # URL to see the orders of a pharmacy
    path('order_delete/<pk>', views.order_delete, name='order_delete'),                                 # URL to delete an order of a pharmacy
    path('confirm_order/<pk>', views.confirm_order, name='confirm_order'),                              # URL to fill an order of a pharmacy
    path('add_product/', views.add_product, name='add_product'),                                        # URL to add a product to a pharmacy
]