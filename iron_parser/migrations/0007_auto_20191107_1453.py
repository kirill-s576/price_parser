# Generated by Django 2.2.5 on 2019-11-07 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iron_parser', '0006_auto_20191009_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcheck',
            name='full_price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='check',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 7, 14, 53, 27, 484505)),
        ),
        migrations.AlterField(
            model_name='check',
            name='variants',
            field=models.TextField(default='', max_length=10000),
        ),
    ]