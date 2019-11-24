from django.shortcuts import render
from iron_parser.models import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from iron_parser.utils import IronParser
import threading
from django.contrib.auth import get_user
from .refresh_functions import *
# Create your views here.


def results_main(request):

    gooses = GooseBase.objects.filter(user__username=get_user(request).username).order_by("name")
    opponents = Opponent.objects.all()
    categories = GooseBase.objects.all().values('category').distinct()
    return render(request, "results/results_main.html", locals())

def results_refresh(request):

    new_refresh()
    refresh_potential_gooses()
    print("Обновление базы успешно завершено")
    return HttpResponseRedirect("/ironparserresults/")


def results_refresh_one(request, goose_id):

    new_refresh(id=goose_id)
    # refresh_potential_gooses(id=goose_id)

    return HttpResponseRedirect("/goose_card/"+str(goose_id))
