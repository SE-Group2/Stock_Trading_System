# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CapitalAccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AccountID', models.CharField(max_length=30)),
                ('Password', models.CharField(max_length=30)),
                ('Isfirst', models.BooleanField(default=1)),
                ('BuyPassword', models.CharField(max_length=30)),
                ('loginPwdWrongNum', models.IntegerField(default=0)),
                ('transPwdWrongNum', models.IntegerField(default=0)),
                ('lastTimeTrans', models.DateTimeField()),
                ('lastTimeLogin', models.DateTimeField()),
                ('IsTransFreeze', models.BooleanField()),
                ('IsLoginFreeze', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SecurityAccountInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SecurityID', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StockInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StockID', models.CharField(max_length=30)),
                ('StockName', models.CharField(max_length=30)),
                ('CurrentPrice', models.FloatField()),
                ('UpLimit', models.FloatField()),
                ('DownLimit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserID', models.CharField(max_length=30)),
                ('Name', models.CharField(max_length=30)),
                ('IDcard', models.CharField(max_length=30)),
                ('Gender', models.IntegerField(max_length=30)),
                ('Occupation', models.CharField(max_length=30)),
                ('EduInfo', models.CharField(max_length=30)),
                ('HomeAddr', models.TextField(max_length=30)),
                ('Department', models.TextField(max_length=30)),
                ('Tel', models.CharField(max_length=30)),
                ('MailAddr', models.CharField(max_length=30)),
                ('Age', models.IntegerField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='capitalaccountinfo',
            name='SecurityAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.SecurityAccountInfo'),
        ),
        migrations.AddField(
            model_name='capitalaccountinfo',
            name='UserTable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.UserTable'),
        ),
    ]
