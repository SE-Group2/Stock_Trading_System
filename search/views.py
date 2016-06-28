#coding:utf8
import threading
from time import sleep

from django.shortcuts import render
from database.models import StockInfo
from .models import StockHistoryInfo
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponse,Http404
import json

# Create your views here.

HasOpened = False


def main(req):
	global  HasOpened
	if  not HasOpened:
		updateDbRegular = UpdateDbRegular()
		updateDbRegular.setDaemon(True)
		updateDbRegular.start()
		HasOpened = True
	list = [
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:00:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:01:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:02:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:03:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:04:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:05:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:06:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:07:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:08:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:09:00 +0800 2015"},
		{"volume": 68246139100, "open": 4660.075, "high": 4814.672, "close": 4813.798, "low": 4656.825, "chg": 156.202,
		 "percent": 3.35, "turnrate": 0.0, "ma5": 4572.931, "ma10": 4461.213, "ma20": 4409.708, "ma30": 4357.837,
		 "dif": 135.68, "dea": 113.37, "macd": 44.62, "time": "Mon May 25 9:10:00 +0800 2015"}
	]
	data = {"symbol": "SHxxxxx", "name": "aaaa", "list": list},
	return render(req, 'stock.html', {"data": json.dumps(data)})


def refresh_5s(req):
	if req.method == 'POST':
		stockinfo = request.POST.get('stockinfo')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
		except StockInfo.DoesNotExist:
			pass
		else:
			return HttpResponse({'StockID':x.StockID,'CurrentPrice':x.CurrentPrice})
	else:
		raise Http404


def refresh_1min(req):
	if req.method == 'POST':
		stockid = req.POST.get('stockid')
		starttime = req.POST.get('starttime')
		endtime = req.POST.get('endtime')
		try:
			x = StockHistoryInfo.objects.filter(StockID=stockid,HistoryTime__gte=starttime,HistoryTime__lte=endtime)
		except StockInfo.DoesNotExist:
			pass
		else:
			return HttpResponse({'history_info':x})
	else:
		raise Http404


def update_realtime(stockcurrentprices):
	try:
		for stockid in stockcurrentprices:
			x = StockInfo.objects.get(StockID=stockid)
			x.CurrentPrice = stockcurrentprices[stockid]
			x.save()
	except StockInfo.DoesNotExist:
		pass


def insert_history(stockhistoryinfo):
	try:
		for stockid in stockhistoryinfo:
			historytime = stockhistoryinfo[stockid][0]
			highestvalue = stockhistoryinfo[stockid][1]
			lowestvalue = stockhistoryinfo[stockid][2]
			x = StockHistoryInfo(StockID=StockInfo.objects.get(StockID="111111"),HistoryTime=historytime,Highest_value=highestvalue,Lowest_value=lowestvalue)
			x.save()
	except StockInfo.DoesNotExist:
		pass


class UpdateDbRegular(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.a = 0

	def run(self):
		while (True):
			self.a = 111111
			dt = datetime.now()
			data = {str(self.a): 12.23}
			# print(data)
			update_realtime(data)
			sleep(5)

