from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .excel import ExcelOrder
from .models import Order
# Create your views here.

def sells_analis(request):
    # ex = ExcelOrder("/parser/price_parser/static/excel/ALL4.xlsx")
    # for i in range(1, 30000, 1):
    #     order = ex.set_order(i)
    #     o = Order()
    #     o.client = order.client
    #     o.date_time = order.date_time
    #     o.price = order.price
    #     o.shop = order.shop
    #     o.bonus_card = order.bonus_card
    #     o.number = order.number
    #     o.worker = order.worker
    #     o.save()
    #     print(str(o.date_time))
    # o = Order.objects.all()
    # o.delete()
    print("123")
    print("123")
    print("123")
    print("123")

    # o = Order.objects.all()
    # array = []
    # a = 0
    # for i in o:
    #     if i.number not in array:
    #         array.append(i.number)
    #     else:
    #         i.delete()
    #     a += 1
    #     print(a)
    return HttpResponseRedirect("/")