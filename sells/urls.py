from django.urls import path
from sells import views

urlpatterns = [
    path('', views.sells_analis, name="sells_analis")

]