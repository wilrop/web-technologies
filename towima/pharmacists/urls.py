from django.urls import path
from django.conf.urls import url
from pharmacists import views

urlpatterns = [
    path('list/', views.pharmacists_list, name='list'),
    url(r'^profile/(?P<pk>\d+)/$', views.pharmacists_profile, name='profile'),
]