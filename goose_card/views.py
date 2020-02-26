from django.shortcuts import render
from iron_parser.models import *
# Create your views here.


def full_card(request, goose_id):
    goose = GooseBase.objects.get(id=goose_id)
    categories = GooseBase.objects.all().values('category').distinct()
    opponents = Opponent.objects.all()
    opponent_gooses = OpponentGoose.objects.filter(goose=goose)
    return render(request, "goose-card/detail-card.html", locals())

def remove_opponent(request, opponent_id):
    return "Успешно"