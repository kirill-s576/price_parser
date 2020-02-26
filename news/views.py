from django.shortcuts import render
from iron_parser.models import GooseBase, Opponent

# Create your views here.

def news_main(request):
    gooses = GooseBase.objects.all().exclude(category="Жидкости").order_by("category")
    opponents = Opponent.objects.all()
    return render(request, "news/news_main.html", locals())