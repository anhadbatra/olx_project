"""olx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from .api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register('message', MessageModelViewSet, base_name='message-api')
router.register('user', UserModelViewSet, base_name='user-api')
urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listing, name='listing'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('myads/', views.myads, name='myads'),
    path('logout/', views.user_logout, name='logout'),
    path('postad/', views.post_ad, name='postad'),
    path('contact/', views.contact, name='contact'),
    path('advertise/<int:id>/', views.advertise, name='advertise'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('editad/<int:id>/' , views.editad,name='editad'),
    path('changepassword/', views.change_pass,name='changepass'),
    path('search/',views.search_item,name='search_item'),
    path('favourites/', views.favourites,name='favourites'),
    path('deletead/<int:id>/', views.deletead, name='delete'),
    path('api/v1/', include(router.urls)),
    path('chat/', login_required(TemplateView.as_view(template_name='chat.html')), name='home1'),


]





