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
    path('get_locations/', views.get_locations, name='get_locations'),
]