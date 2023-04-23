"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('lineapi/', views.lineapi, name='lineapi'),
    path('homepage/', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('booking/', views.booking_item, name='booking_item'),
    path('mybooking/', views.mybooking, name='mybooking'),
    path('search/', views.search, name='search'),
    path('category/', views.category, name='category'),
    path('profile/', views.profile, name='profile'),
    path('service/', views.service, name='service'),
    path('history/', views.history, name='history'),
]