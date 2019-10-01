from django.urls import path
from authorisation import views

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('authorisation/', views.authorisation, name="authorisation")

]