"""towima URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Necessary imports for the urls
from django.contrib import admin
from django.urls import path, include
from towima import views

urlpatterns = [
    path('', views.home, name='home'),                              # The url for the homepage is empty
    path('admin/', admin.site.urls, name='admin'),                  # The url for the admin page
    path('accounts/', include('django.contrib.auth.urls')),         # The url where the accounts app runs
    path('accounts/', include('accounts.urls')),                    # This url pattern will be visitid for the signup and profile functionality
    path('pharmacists/', include('pharmacists.urls')),              # The url where the pharmacists app is
    path('products/', include('products.urls')), # The url where the products app is
]

