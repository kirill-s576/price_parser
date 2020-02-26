from django.db import models
from django.utils import timezone
# Create your models here.
from datetime import datetime
from django.contrib.auth.models import User
from news.models import PotentialGoose
# import news
import json


class GooseBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    keys = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    manufacturer = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, default="Разное")
    image = models.URLField(default='/static/image/no_image.png')

    def __str__(self):
        return self.name

    def last_subchecks(self):
        try:
            last_check = Check.objects.filter(goose=self).order_by('-date')[0]
            subchecks = SubCheck.objects.filter(check_name=last_check)
        except:
            subchecks = ""
        return subchecks

    def get_price_list(self):
        try:
            price_list = []
            last_check = Check.objects.filter(goose=self).order_by('-date')[0]
            subchecks = SubCheck.objects.filter(check_name=last_check)#.exclude(opponent_goose__opponent_name__name='SigaretNet')
            for subcheck in subchecks:
                price_list.append(float(subcheck.price))
            return sorted(price_list)
        except:
            return [0]

    def get_base_price(self):
        try:
            base_price = []
            last_check = Check.objects.filter(goose=self).order_by('-date')[0]
            subchecks = SubCheck.objects.filter(check_name=last_check, opponent_goose__opponent_name__name='SigaretNet')

            for subcheck in subchecks:
                base_price.append(subcheck.price)
            return sorted(base_price)
        except:
            return [0]

    def info_for_chart(self):
        op_gooses = OpponentGoose.objects.filter(goose=self)

        result = {}
        for op_goose in op_gooses:
            result[op_goose.opponent_name.name] = op_goose.get_price_changes()
        result1 = json.dumps(result)
        return result1

    def get_categories(self):
        categories = GooseBase.objects.all().values('category').distinct()
        print(categories)
        return categories

    def min_price(self):
        try:
            op_gooses = OpponentGoose.objects.filter(goose=self)
            current_price_list = []
            for op_goose in op_gooses:
                last_subcheck = op_goose.last_subcheck()
                if last_subcheck.price != 0:
                    current_price_list.append(last_subcheck.price)
            return min(current_price_list)
        except:
            return 0

    def max_price(self):
        try:
            op_gooses = OpponentGoose.objects.filter(goose=self)
            current_price_list = []
            for op_goose in op_gooses:
                last_subcheck = op_goose.last_subcheck()
                current_price_list.append(last_subcheck.price)
            return max(current_price_list)
        except:
            return 0

    def current_rating(self):
        min = self.min_price()
        max = self.max_price()
        center = int((min+max)/2)
        try:
            base = self.get_base_price()[0]
        except:
            base = max

        price_list = self.get_price_list()
        try:
            base_index = price_list.index(base)
        except:
            base_index = -1


        try:
            return (100-int((base-min)/(max-min)*100)+1)
        except:
            return 1

    def potential_gooses(self):
        new_potential_gooses = PotentialGoose.objects.filter(goose=self, confirmed=False)
        return new_potential_gooses

    def potential_entity(self):
        new_potential_gooses = PotentialGoose.objects.filter(goose=self, confirmed=False)
        return len(new_potential_gooses)

class Opponent(models.Model):
    name = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class OpponentGoose(models.Model):
    goose = models.ForeignKey(GooseBase, on_delete=models.CASCADE)
    opponent_name = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=1000)
    url = models.URLField(max_length=1000)
    available = models.BooleanField(default=False)
    img = models.URLField(default='/static/image/no_image.png')

    def __str__(self):
        return str(self.goose.name) + "/" + str(self.opponent_name)

    def get_price_changes(self):

        subchecks = SubCheck.objects.filter(opponent_goose=self).order_by('check_name__date')
        changes_array = []
        now_price = 0
        for subcheck in subchecks:
            check = Check.objects.get(subcheck=subcheck)

            if subcheck.price == now_price:
                pass
            else:
                now_price = subcheck.price
                # date = str(check.date.date().year) + "-" + \
                #        str(check.date.date().month) + "-" + \
                #        str(check.date.date().day)
                date = check.date.strftime("%Y/%m/%d,%H:%M:%S")
                changes_array.append({date: subcheck.price})
        # Удаляем даты
        changes_array.reverse()
        cur_date = ""
        cur_price = 0
        for i in changes_array:
            date = list(i.keys())[0]
            price = i[date]
            if date == cur_date:
                changes_array.remove(i)
            cur_date = date
            cur_price = price
        changes_array.reverse()
        for i in changes_array:
            print(list(i.keys())[0])
        return changes_array

    def last_subcheck(self):
        subcheck = SubCheck.objects.filter(opponent_goose=self).order_by('check_name__date').reverse().first()
        return subcheck


class Check(models.Model):
    goose = models.ForeignKey(GooseBase, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    variants = models.TextField(max_length=10000, default="")  # Массив вариантов, которые выдал поиск.(JSON)

    def __str__(self):
        return str(self.goose.name) + "/" + str(self.date)


class SubCheck(models.Model):
    check_name = models.ForeignKey(Check, on_delete=models.CASCADE)
    opponent_goose = models.ForeignKey(OpponentGoose, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    full_price = models.FloatField(default=0)
    available = models.CharField(max_length=100, default="Не обновлено")

    def __str__(self):
        return str(self.opponent_goose.local_name) + "/" + str(self.check_name.date.date())

    def get_check(self):
        return Check.objects.get(subcheck=self)

    def action(self):
        try:
            return int((self.full_price - self.price)/self.full_price*100)
        except:
            return 0

    def get_opponent(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.opponent_name

    def get_localname(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.local_name

    def get_url(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.url

    def get_available(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.available

    def get_price_changes(self):
        subchecks = SubCheck.objects.filter(opponent_goose=self.opponent_goose).order_by('check_name__date')
        changes_array = []
        now_price = 0
        for subcheck in subchecks:
            check = Check.objects.get(subcheck=subcheck)

            if subcheck.price == now_price:
                pass
            else:
                now_price = subcheck.price
                date = str(check.date.date().day) + "." + \
                       str(check.date.date().month) + "." + \
                       str(check.date.date().year)
                changes_array.append({date: subcheck.price})

        return changes_array

