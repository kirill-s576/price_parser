from django.db import models
import datetime
# from iron_parser.models import *
# Create your models here.
import iron_parser

# class New(models.Model):
#
#     name = models.CharField(max_length=200)
#     datetime = models.DateTimeField(default=datetime.datetime.now)
#     text = models.TextField()
#     category = models.CharField(max_length=100)
#     goose = models.ForeignKey(GooseBase, on_delete=models.CASCADE, default=None)
#     opponent = models.ForeignKey(Opponent, on_delete=models.CASCADE, default=None)
#     # Просмотрена или не просмотрена
#     check = models.BooleanField(default=False)
#     # Статус(Обработана или не обработана)
#     status = models.BooleanField(default=False)


class PotentialGoose(models.Model):
    goose = models.ForeignKey('iron_parser.GooseBase', on_delete=models.CASCADE, default=None)
    template = models.CharField(max_length=400)
    opponent = models.ForeignKey('iron_parser.Opponent', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=400)
    url = models.URLField(max_length=500, default="")
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.opponent.name + self.name + str(self.created_at)
