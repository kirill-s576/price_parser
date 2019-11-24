from django.urls import path
from authorisation import views

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('logout/', views.log_out, name="logout"),
    path('enter/', views.enter, name="enter"),
    path('', views.authorisation, name="authorisation")

]