#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserTable(models.Model):
	UserID = models.CharField(max_length=30)
	Name = models.CharField(max_length=30)
	IDcard = models.CharField(max_length=30)
	Gender = models.IntegerField()
	Occupation = models.CharField(max_length=30)
	EduInfo = models.CharField(max_length=30)
	HomeAddr = models.TextField(max_length=30)
	Department = models.TextField(max_length=30)
	Tel = models.CharField(max_length=30)
	MailAddr = models.CharField(max_length=30)
	Age = models.IntegerField()

class SecurityAccountInfo(models.Model):
	SecurityID = models.CharField(max_length=30)

class CapitalAccountInfo(models.Model):
	AccountID = models.CharField(max_length=30)
	Password = models.CharField(max_length=30)
	Isfirst = models.BooleanField(default=1)
	UserTable = models.ForeignKey(UserTable)
	BuyPassword = models.CharField(max_length=30)
	SecurityAccount = models.ForeignKey(SecurityAccountInfo)
	loginPwdWrongNum = models.IntegerField(default=0)
	transPwdWrongNum = models.IntegerField(default=0)
	lastTimeTrans = models.DateTimeField()
	lastTimeLogin = models.DateTimeField()
	IsTransFreeze = models.BooleanField()
	IsLoginFreeze = models.BooleanField()

class StockInfo(models.Model):
	StockID = models.CharField(max_length=30)
	StockName = models.CharField(max_length=30)
	CurrentPrice = models.FloatField()
	UpLimit = models.FloatField()
	DownLimit = models.FloatField()
