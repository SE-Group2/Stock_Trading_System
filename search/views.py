#coding:utf8
from django.shortcuts import render
from database.models import StockInfo
from .models import StockHistoryInfo
from django.db.models import Q

# Create your views here.

def main(req):
	return render(req,'search.html')

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
	for stockid in stockhistoryinfo:
		historytime = stockhistoryinfo[stockid][0]
		highestvalue = stockhistoryinfo[stockid][1]
		lowestvalue = stockhistoryinfo[stockid][2]
		x = StockHistoryInfo(StockID=stockid,HistoryTime=historytime,Highest_value=highestvalue,Lowest_value=lowestvalue)
		x.save()
	
