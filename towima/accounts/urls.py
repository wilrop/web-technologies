from django.urls import path
from accounts import views

urlpatterns = [ 
    path('signup/', views.signup, name='signup'),                   # The url for the signup page
]