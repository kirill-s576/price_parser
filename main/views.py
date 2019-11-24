from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from iron_parser.models import *

# Create your views here.
def new_main(request):
    user = auth.get_user(request)
    gooses = GooseBase.objects.filter(user=user)
    if user.is_authenticated:
        return render(request, 'main/main_base.html', locals())
    else:
        return HttpResponseRedirect('/authorisation/')

def main(request):
    user = auth.get_user(request)
    # gooses = GooseBase.objects.filter(user=user)
    categories = GooseBase.objects.all().values('category').distinct()

    if user.is_authenticated:
        return render(request, 'main/main_base_new.html', locals())
    else:
        return HttpResponseRedirect('/authorisation/')


def main_cat(request, category):
    user = auth.get_user(request)
    print(category)
    gooses = GooseBase.objects.filter(category=category, user=user)
    categories = GooseBase.objects.all().values('category').distinct()
    if user.is_authenticated:
        return render(request, 'main/main_base_new.html', locals())
    else:
        return HttpResponseRedirect('/authorisation/')
