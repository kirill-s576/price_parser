from django.urls import path, re_path
from results import views

urlpatterns = [
    re_path(r'refresh/(?P<goose_id>\d+)', views.results_refresh_one),
    path('refresh/', views.results_refresh, name="iron_parser_results_refresh"),
    path('', views.results_main, name="iron_parser_results_main")

]