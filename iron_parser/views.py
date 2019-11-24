from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import *
from .utils import IronParser
from django.contrib.auth import get_user
from django.contrib.auth.models import User
import json
from news.models import PotentialGoose
# Create your views here.


def main(request):
    gooses = GooseBase.objects.all()
    categories = gooses.values_list('category').distinct
    return render(request, "iron_parser/iron_parser_content.html", locals())


def parse(request):
    key = request.POST['keys']
    print(key)
    parser = IronParser(key)
    i = parser.get_all_parse()
    return render(request, "iron_parser/iron_parser_results.html", locals())


def create_goose(request):
    data = request.POST
    print(data)
    user = get_user(request)
    user_model = User.objects.get(username=user.username)
    if int(data['id']) > 0:
        goose = GooseBase.objects.get(id=int(data['id']))
        for opponent_goose in eval(data['data']):
            op_name = Opponent.objects.get(name=opponent_goose["parent"])
            op_goose = OpponentGoose(goose=goose, opponent_name=op_name, local_name=opponent_goose["name"], url=opponent_goose["url"])
            print(op_goose)
            op_goose.save()
            print("Добавлен новый товар-конкурент.")
    else:
        goose = GooseBase(name=data['name'], keys=data['keys'], category=data["category"], user=user_model)
        goose.save()
        # parser = IronParser(data['keys'])
        # i = parser.get_all_parse()
        # fist_check = Check(goose=goose, variants=i)
        # fist_check.save()
        for opponent_goose in eval(data['data']):
            op_name = Opponent.objects.get(name=opponent_goose["parent"])
            op_goose = OpponentGoose(goose=goose, opponent_name=op_name, local_name=opponent_goose["name"], url=opponent_goose["url"])
            print(op_goose)
            op_goose.save()
            # sub = SubCheck(check_name=fist_check, price=float(opponent_goose["price"]), opponent_goose=op_goose)
            # sub.save()
    return HttpResponse(json.dumps({'status': "Ok"}), content_type='application/json')


def remove_op(request):
    op_id = request.POST["op_id"]
    op_goose = OpponentGoose.objects.get(id=op_id)
    op_goose.delete()
    return HttpResponse(json.dumps({'status': "Ok"}), content_type='application/json')

def find_goose(request):
    template = request.POST["template"]
    print(template)
    gooses = GooseBase.objects.filter(name__icontains=template, user=get_user(request))
    print(gooses)
    return render(request, "main/goose_cards_content.html", locals())

def remove_potential(request):
    print("Удаляем товар")
    potential_id = request.POST["id"]
    potential = PotentialGoose.objects.get(id=potential_id)
    potential.confirmed = True
    potential.viewed = True
    potential.removed = True
    potential.save()
    return HttpResponse(json.dumps({'status': "Ok"}), content_type='application/json')

def add_potential(request):
    print("Lj,fdkztv товар")
    potential_id = request.POST["id"]
    goose_id = request.POST["goose_id"]
    potential = PotentialGoose.objects.get(id=potential_id)
    # Требуется добавить новый товар оппонент к существующему товару
    goose = GooseBase.objects.get(id=goose_id)
    op_goose = OpponentGoose(goose=goose, opponent_name=potential.opponent, local_name=potential.name,
                             url=potential.url)
    print(op_goose)
    op_goose.save()
    potential.confirmed = True
    potential.viewed = True
    potential.save()
    return HttpResponse(json.dumps({'status': "Ok"}), content_type='application/json')

def remove_all_potential(request):
    goose_id = request.POST["goose_id"]
    goose = GooseBase.objects.get(id=goose_id)
    potentials = PotentialGoose.objects.filter(goose=goose)
    for potential in potentials:
        potential.confirmed = True
        potential.viewed = True
        potential.removed = True
        potential.save()
    return HttpResponse(json.dumps({'status': "Ok"}), content_type='application/json')