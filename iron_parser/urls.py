from django.urls import path
from iron_parser import views

urlpatterns = [
    path('parse/', views.parse, name="iron_parser_parse"),
    path('create_goose/', views.create_goose, name="iron_parser_create_goose"),
    path('', views.main, name="iron_parser_main")

]