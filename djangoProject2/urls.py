"""djangoProject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views
from core.views import *
from core.api import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',frontpage,name='frontpage'),
    path('signup/',register,name='signup'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('login/',views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('feed/',feed,name='feed'),
    path('api/add_post',api_add_post,name='api_add_post'),
    path('api/add_like/',api_add_like,name='api_add_like'),
    path('search/',search,name='search'),
    path('u/<str:username>/',profile,name='profile'),
    path('u/<str:username>/follow/',follow,name='follow'),
    path('u/<str:username>/unfollow/',unfollow,name='unfollow'),
    path('u/<str:username>/followers/', followers, name='followers'),
    path('u/<str:username>/follows/', follows, name='follows'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('notifications/', notifications, name='notifications'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)