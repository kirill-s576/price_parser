from django.shortcuts import render
from authorisation.models import Profile, User
from django.contrib.auth import *
from django.http import HttpResponse, HttpResponseRedirect
import re
import urllib.request
import json

def get_html(url):
    resp = urllib.request.urlopen(url)
    return resp.read().decode("utf8")

def authorisation(request):

        get_user(request)

        price = get_user(request)
        if price.is_anonymous:
            p = "Анонимный польователь"
        else:
            p = Profile.objects.get(user=price)
        return render(request, "authorisation/entry_block.html", locals())

def registration(request):
    if request.POST:
        print(request.POST)
        return HttpResponse(request)
    else:
        return render(request, "authorisation/registration_block.html", locals())