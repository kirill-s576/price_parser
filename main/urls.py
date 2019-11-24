from django.urls import path, re_path
from django.conf.urls import url, include
from main import views


urlpatterns = [
    re_path(r'category/(?P<category>[\s\w]+)', views.main_cat),
    path('', views.main)
]