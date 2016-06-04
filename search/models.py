from __future__ import unicode_literals

from django.db import models
from database.models import StockInfo

# Create your models here.
class StockHistoryInfo(models.Model):
	StockID = models.ForeignKey(StockInfo)
	HistoryTime = models.DateTimeField()
	Highest_value = models.FloatField()
	Lowest_value = models.FloatField()
