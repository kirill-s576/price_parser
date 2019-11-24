from django.urls import re_path
from goose_card import views

urlpatterns = [

    re_path(r'(?P<goose_id>\d+)', views.full_card, name="full_goose_card")

]