from django.urls import path
from iron_parser import views

urlpatterns = [
    path('remove_all_potential/', views.remove_all_potential),
    path('add_potential/', views.add_potential),
    path('remove_potential/', views.remove_potential),
    path('find_goose/', views.find_goose),
    path('remove_op_goose/', views.remove_op),
    path('parse/', views.parse, name="iron_parser_parse"),
    path('create_goose/', views.create_goose, name="iron_parser_create_goose"),
    path('', views.main, name="iron_parser_main")

]