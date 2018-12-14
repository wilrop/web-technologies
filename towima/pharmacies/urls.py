from django.urls import path
from django.conf.urls import url
from pharmacies import views

app_name = 'pharmacies'
urlpatterns = [
    path('create_pharma/', views.create_pharma, name='create_pharma'),
    path('search/', views.search, name='search'),
    url(r'^pharmacy/(?P<pk>\d+)/$', views.pharmacy, name='pharmacy'),
    url(r'^pharmacy/(?P<pk>\d+)/comment/$', views.add_comment_to_pharmacy, name='add_comment_to_pharmacy'),
    url(r'^pharmacy/(?P<pk>\d+)/rating/(?P<new_rating>\d+)/$', views.add_rating_to_pharmacy, name='add_rating_to_pharmacy'),
]