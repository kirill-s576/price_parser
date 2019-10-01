from django.urls import path, re_path
from django.conf.urls import url, include
from main import views


urlpatterns = [

    path('', views.main)
]