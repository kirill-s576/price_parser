from django.urls import path
from news import views

urlpatterns = [
    path('', views.news_main, name="iron_parser_news_main")
]