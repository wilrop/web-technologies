from django.urls import path
from accounts import views

urlpatterns = [ 
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),                                   # The url for the signup page. 
    path('validate_username/', views.validate_username, name='validate_username'),  # The url to validate the username.
    path('phone_verification', views.phone_verification, name='phone_verification'),# The url that is used for the phone_verification.
    path('verify/', views.verify, name='verify'),                                   # The url for the verify page.                            
    path('profile/', views.profile, name='profile'),                                # The url for the profile page.                           
    path('profile/edit/', views.edit_profile, name='edit'),                         # The url for the edit profile page.                      
    path('change-password/', views.change_password, name='change-password'),        # The url for the change password page.
    path('orders/', views.orders, name='orders'),                                   # The url for displaying the open/filled orders.
    path('cart/', views.cart, name='cart'),                                         # The url for displaying the cart.
    path('item_delete/<pk>', views.item_delete, name='item_delete'),                # The url for deleting an item in the cart. 
    path('order_delete/<pk>', views.order_delete, name='order_delete'),             # The url for deleting an open order in the account.
    path('place_orders', views.place_orders, name='place_orders'),                  # The url for ordering the items in the cart.
]