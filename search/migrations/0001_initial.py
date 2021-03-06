# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0002_auto_20160604_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockHistoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HistoryTime', models.DateTimeField()),
                ('Highest_value', models.FloatField()),
                ('Lowest_value', models.FloatField()),
                ('StockID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.StockInfo')),
            ],
        ),
    ]
