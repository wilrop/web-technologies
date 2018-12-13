from django.urls import path
from django.conf.urls import url
from pharmacies import views

app_name = 'pharmacies'
urlpatterns = [
    path('create_pharma/', views.create_pharma, name='create_pharma'),
    path('search/', views.search, name='search'),
    url(r'^pharmacy/(?P<pk>\d+)/$', views.pharmacy, name='pharmacy'),
]