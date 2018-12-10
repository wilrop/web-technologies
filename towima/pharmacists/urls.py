from django.urls import path
from django.conf.urls import url
from pharmacists import views

urlpatterns = [
    path('list/', views.pharmacists_list, name='list'),
    path('find_pharma/', views.find_pharma, name='findpharma' ),
    url(r'^profile/(?P<pk>\d+)/$', views.pharmacists_profile, name='profile'),
    url(r'^profile/(?P<pk>\d+)/comment/$', views.add_comment_to_profile, name='add_comment_to_profile'),
]