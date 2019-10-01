from django.db import models
from django.utils import timezone
# Create your models here.
from datetime import datetime

class GooseBase(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    keys = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="Разное")
    def __str__(self):
        return self.name


class Opponent(models.Model):
    name = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class OpponentGoose(models.Model):
    goose = models.ForeignKey(GooseBase, on_delete=models.CASCADE)
    opponent_name = models.ForeignKey(Opponent, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=100)
    url = models.URLField(max_length=1000)
    def __str__(self):
        return self.goose.name


class Check(models.Model):
    goose = models.ForeignKey(GooseBase, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    variants = models.CharField(max_length=1000)  # Массив вариантов, которые выдал поиск.(JSON)


class SubCheck(models.Model):
    check_name = models.ForeignKey(Check, on_delete=models.CASCADE)
    opponent_goose = models.ForeignKey(OpponentGoose, on_delete=models.CASCADE)
    price = models.FloatField(default=0)

    def get_opponent(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.opponent_name

    def get_localname(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.local_name

    def get_url(self):
        a = OpponentGoose.objects.get(subcheck=self)
        return a.url