from django.shortcuts import render
from authorisation.models import Profile, User
from django.contrib.auth import login, logout, get_user
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

def authorisation(request):
        user = get_user(request)

        if user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return render(request, "authorisation/entry_block.html", locals())


def enter(request):
    try:
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return HttpResponseRedirect('/')
    except:
        message = "Неправильно введен логин или пароль"
        return render(request, "authorisation/entry_block.html", locals())

def registration(request):
    if request.POST:
        print(request.POST)
        return HttpResponse(request)
    else:
        return render(request, "authorisation/registration_block.html", locals())

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/authorisation/')