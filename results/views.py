from django.shortcuts import render
from iron_parser.models import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from iron_parser.utils import IronParser

# Create your views here.


def results_main(request):
    gooses = GooseBase.objects.all().order_by("name")
    opponents = Opponent.objects.all()
    op_gooses = OpponentGoose.objects.all()
    a = op_gooses.values('url').distinct()
    print(a)
    return render(request, "results/results_main.html", locals())

def results_refresh(request):
    gooses = GooseBase.objects.all()
    for goose in gooses:
        keys = goose.keys
        parser = IronParser(keys)
        parse = parser.get_all_parse()
        # Создаем новый чек и сохраняем результаты поиска.
        check = Check(goose=goose, variants=parse)
        check.save()
        opponent_gooses = OpponentGoose.objects.filter(goose=goose)
        for opponent_goose in opponent_gooses:
            for shop in parse:
                for find_goose in parse[shop]:
                    if find_goose["name"] == opponent_goose.local_name:
                        sub = SubCheck(check_name=check, price=float(find_goose["price"]), opponent_goose=opponent_goose)
                        sub.save()

    return HttpResponseRedirect("/ironparserresults/")