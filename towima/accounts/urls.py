from django.urls import path
from accounts import views

urlpatterns = [ 
    path('signup/', views.signup, name='signup'),                               # The url for the signup page.                               
    path('profile/', views.profile, name='profile'),                            # The url for the profile page.                           
    path('profile/edit/', views.edit_profile, name='edit'),                     # The url for the edit profile page.                      
    path('change-password/', views.change_password, name='change-password'),    # The url for the change password page.
]