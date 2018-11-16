from django.urls import path
from django.conf.urls import url
from pharmacists import views

urlpatterns = [
    path('list/', views.pharmacists_list, name='list'),
    path('find_pharma/', views.find_pharma, name='findpharma' ),
    path('create_pharma/', views.create_pharmacy, name='create_pharmacy'),
    #path('profile/', views.pharmacists_profile, name='profile'),
    
    url(r'^profile/(?P<pk>\d+)/$', views.pharmacists_profile, name='profile')
]