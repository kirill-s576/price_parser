from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .utils import IronParser
import json

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
    goose = GooseBase(name=data['name'], keys=data['keys'], category=data["category"])
    goose.save()

    parser = IronParser(data['keys'])
    i = parser.get_all_parse()
    fist_check = Check(goose=goose, variants=i)
    fist_check.save()
    for opponent_goose in eval(data['data']):
        op_name = Opponent.objects.get(name=opponent_goose["parent"])
        op_goose = OpponentGoose(goose=goose, opponent_name=op_name, local_name=opponent_goose["name"], url=opponent_goose["url"])
        print(op_goose)
        op_goose.save()
        sub = SubCheck(check_name=fist_check, price=float(opponent_goose["price"]), opponent_goose=op_goose)
        sub.save()
    return render(request, "iron_parser/iron_parser_create_goose.html", locals())
