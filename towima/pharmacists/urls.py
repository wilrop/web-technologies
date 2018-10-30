from django.urls import path
from pharmacists import views

urlpatterns = [
    path('list/', views.pharmacists_list, name='list')
]