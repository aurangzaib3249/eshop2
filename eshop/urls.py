"""eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path('admin/', admin.site.urls),
    path('seller/',include("Seller.urls"),name="seller"),
    path('accounts/',include("Accounts.urls"),name="accounts"),
    path('buyer/',include("Buyer.urls"),name="buyer"),
    path('chat/', chat_home, name='chat'),
    path('video/', video_chat, name='video'),
    path('create_group', create_group, name='create_group'),
    path('chat/<str:chat_with>/', chat_with_user, name='chat_with'),
    path('chat/group/<str:chat_with>/', chat_with_groups, name='chat_with_groups'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
