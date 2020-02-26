from django.db import models
import datetime
from django.utils import timezone
# Create your models here.


class Order(models.Model):
    number = models.CharField(max_length=50)
    date_time = models.DateTimeField(default=timezone.now())
    shop = models.CharField(max_length=200, null=True)
    client = models.CharField(max_length=200, null=True)
    bonus_card = models.CharField(max_length=200, null=True)
    price = models.FloatField(default=0, null=True)
    worker = models.CharField(max_length=200, null=True)


