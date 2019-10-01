from django.shortcuts import render

# Create your views here.

def news_main(request):

    return render(request, "news/news_main.html", locals())