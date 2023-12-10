"""CrossBorderECommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Autoresponder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("Autoresponder/", include("Autoresponder.urls")),
    # path('register/', views.register, name='register'),
    # path('user_login/', views.user_login, name='user_login'),
    # path('settle_payment/', views.settle_payment, name='settle_payment'),
    # path('index/', views.index, name='index'),
    # path('base/', views.base, name='base'),
    # path('main/', views.main, name='main'),
    # path('auto_reply_settings/', views.save_settings, name='save_settings'),
    # path('start_auto_reply/', views.start_auto_reply, name='start_auto_reply'),
    # path('stop_auto_reply/', views.stop_auto_reply, name='stop_auto_reply'),
    # path('get_saved_settings/', views.get_saved_settings, name='get_saved_settings'),
    # path('async_view/', views.async_view, name='async_view'),
]
