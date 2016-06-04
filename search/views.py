#coding:utf8
import threading
from time import sleep

from django.shortcuts import render
from database.models import StockInfo
from .models import StockHistoryInfo
from django.db.models import Q
from datetime import datetime

# Create your views here.

HasOpened = False

def main(req):
	global  HasOpened
	if  not HasOpened:
		updateDbRegular = UpdateDbRegular()
		updateDbRegular.setDaemon(True)
		updateDbRegular.start()
		HasOpened = True

	return render(req,'stock.html')

def refresh_5s(req):
	stockinfo = req.stockinfo
	try:
		x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
	except StockInfo.DoesNotExist:
		pass
	else:
		return render(req,'refresh_5s.html',{'StockID':x.StockID,'CurrentPrice':x.CurrentPrice})

def refresh_1min(req):
	stockid = req.stockid
	starttime = req.starttime
	endtime = req.endtime
	try:
		x = StockHistoryInfo.objects.filter(StockID=stockid,HistoryTime__gte=starttime,HistoryTime__lte=endtime)
	except StockInfo.DoesNotExist:
		pass
	else:
		return render(req,'refresh_1min.html',{'history_info':x})

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

