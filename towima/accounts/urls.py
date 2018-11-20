from django.urls import path
from accounts import views

urlpatterns = [ 
    path('signup/', views.signup, name='signup'),                   # The url for the signup page
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit'),
]