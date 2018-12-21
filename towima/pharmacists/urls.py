from django.urls import path
from django.conf.urls import url
from pharmacists import views

urlpatterns = [
    path('list/', views.pharmacists_list, name='list'),                                 # URL to see all the pharmacists
    url(r'^profile/(?P<pk>\d+)/$', views.pharmacists_profile, name='profile'),          # URL to see a profile of a pharmacists
]