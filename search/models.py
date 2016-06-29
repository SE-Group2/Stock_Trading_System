from __future__ import unicode_literals

from django.db import models

class StockInfo(models.Model):
	StockID = models.CharField(max_length=30)
	StockName = models.CharField(max_length=30)
	CurrentPrice = models.FloatField()
	A_D = models.FloatField()
	UpLimit = models.FloatField()
	DownLimit = models.FloatField()

	def __str__(self):
		return self.StockName


# Create your models here.
class StockHistoryInfo(models.Model):
	StockID = models.ForeignKey(StockInfo)
	HistoryTime = models.DateTimeField()
	Open_value = models.FloatField()
	Close_value = models.FloatField()
	Highest_value = models.FloatField()
	Lowest_value = models.FloatField()
	Volume_value = models.FloatField()
	EMA12 = models.FloatField()
	EMA26 = models.FloatField()
	DIF = models.FloatField()
	MACD = models.FloatField()

	def __str__(self):
		return self.StockID.StockName + " " +self.HistoryTime.strftime("%a %b %d %H:%M:%S +0800 %Y")

