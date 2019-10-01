from django.urls import path
from results import views

urlpatterns = [
    path('refresh/', views.results_refresh, name="iron_parser_results_refresh"),
    path('', views.results_main, name="iron_parser_results_main")

]