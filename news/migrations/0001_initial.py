# Generated by Django 2.2.5 on 2019-11-15 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('iron_parser', '0010_auto_20191115_2153'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialGoose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.CharField(max_length=400)),
                ('name', models.CharField(max_length=400)),
                ('url', models.URLField(default='')),
                ('price', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('viewed', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('removed', models.BooleanField(default=False)),
                ('goose', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='iron_parser.GooseBase')),
                ('opponent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='iron_parser.Opponent')),
            ],
        ),
    ]