#coding:utf8
import threading
from time import sleep

from django.shortcuts import render
from database.models import StockInfo
from .models import StockHistoryInfo
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponse,Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from search.models import StockHistoryInfo
from database.models import StockInfo
from datetime import datetime
import json
import random

# Create your views here.

HasOpened = False

def JsonWrap(historyinfo):
	list = []
	for i in historyinfo:
		s = i.HistoryTime.strftime("%a %b %d %H:%M:%S +0800 %Y")
		x = {"volume":i.Volume_value,"open":i.Open_value,"high":i.Highest_value,"close":i.Close_value,"low":i.Lowest_value,"time":s}
		list.append(x)
	list.reverse()
	data = {"symbol":"SHxxxxx","name":"aaaa","list":list}
	return data

@csrf_exempt
def main(req):
	global  HasOpened
	if  not HasOpened:
		updateDbRegular = UpdateDbRegular()
		updateDbRegular.setDaemon(True)
		updateDbRegular.start()
		HasOpened = True
	if req.method == 'POST':
		stockinfo = req.POST.get('value')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
			historyinfo = StockHistoryInfo.objects.filter(StockID=x).order_by('-HistoryTime')[:100]
		except StockInfo.DoesNotExist:
			pass
		except StockHistoryInfo.DoesNotExist:
			pass
	else:
		pk = random.randint(1,StockInfo.objects.count())
		try:
			x = StockInfo.objects.all()[pk-1]
			historyinfo = StockHistoryInfo.objects.filter(StockID=x).order_by('-HistoryTime')[:100]
		except StockInfo.DoesNotExist:
			pass
		except StockHistoryInfo.DoesNotExist:
			pass
	return render(req,'stock.html',{"stockid":x.StockID,"stockname":x.StockName,"data":json.dumps(JsonWrap(historyinfo))})

@csrf_exempt
def refresh_5s(req):
	if req.method == 'POST':
		stockinfo = req.POST.get('value')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
		except StockInfo.DoesNotExist:
			pass
		else:
			return JsonResponse({'result':1,'CurrentPrice':x.CurrentPrice,'A_D':x.A_D,'State':"Normal"})
	res = {}
	res["result"] = 0
	return JsonResponse(res)

@csrf_exempt
def refresh_1min(req):
	if req.method == 'POST':
		stockinfo = req.POST.get('value')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
			historyinfo = StockHistoryInfo.objects.filter(StockID=x).order_by('-HistoryTime')[:100]
		except StockInfo.DoesNotExist:
			pass
		except StockHistoryInfo.DoesNotExist:
			pass
		else:
			return JsonResponse({"result":1,"data":JsonWrap(historyinfo)})
	else:
		res = {}
		res["result"] = 0
		return JsonResponse(res)


def search_history(req):
	if req.method == 'POST':
		stockid = req.POST.get('stockid')
		starttime = req.POST.get('starttime')
		endtime = req.POST.get('endtime')
		try:
			historyinfo = StockHistoryInfo.objects.filter(StockID=stockid,HistoryTime__gte=starttime,HistoryTime__lte=endtime)
		except StockInfo.DoesNotExist:
			pass
		else:
			return JsonResponse({"result":1,'history_info':JsonWrap(historyinfo)})
	else:
		res = {}
		res["result"] = 0
		return JsonResponse(res)

def update_realtime(stockcurrentdata):
	try:
		for stockid in stockcurrentdata:
			x = StockInfo.objects.get(StockID=stockid)
			x.CurrentPrice = stockcurrentdata[stockid][0]
			x.A_D = stockcurrentdata[stockid][1]
			x.save()
	except StockInfo.DoesNotExist:
		pass


def insert_history(stockhistoryinfo):
	print stockhistoryinfo
	try:
		for stockid in stockhistoryinfo:
			t = StockInfo.objects.get(StockID=stockid)
			last_record = StockHistoryInfo.objects.filter(StockID=t).order_by('-HistoryTime')[0]
			historytime = stockhistoryinfo[stockid][0]
			openvalue = stockhistoryinfo[stockid][1]
			closevalue = stockhistoryinfo[stockid][2]
			highestvalue = stockhistoryinfo[stockid][3]
			lowestvalue = stockhistoryinfo[stockid][4]
			volume = stockhistoryinfo[stockid][5]
			EMA12 = last_record.EMA12*11/13 + closevalue*2/13
			EMA26 = last_record.EMA12*25/27 + closevalue*2/27
			DIF = EMA12 - EMA26
			MACD = last_record.MACD*8/10 + DIF*2/10
			x = StockHistoryInfo(StockID=t,HistoryTime=historytime,Open_value=openvalue,Close_value=closevalue,Highest_value=highestvalue,Lowest_value=lowestvalue,Volume_value=volume,EMA12=EMA12,EMA26=EMA26,DIF=DIF,MACD=MACD)
			x.save()
	except StockInfo.DoesNotExist:
		pass
	except StockHistoryInfo.DoesNotExist:
		pass

class UpdateDbRegular(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.a = 0

	def run(self):
		count = 0;
		stockid = ["111111","222222","333333"]
		openvalue = []
		closevalue = []
		maxvalue = []
		minvalue = []
		volume = []
		data = {}
		currentprice = []
		print "Thread start"
		for i in xrange(3):
			openvalue.append(10)
			closevalue.append(10)
			maxvalue.append(0)
			minvalue.append(100)
			volume.append(0)
			currentprice.append(10)

		while (True):
			for i in xrange(3):
				A_D = random.random()*0.2-0.1
				if currentprice[i] <= 5 and A_D <0:
					A_D = -A_D;
				rd = A_D*currentprice[i]
				currentprice[i] = currentprice[i] + rd
				data[stockid[i]] = [currentprice[i],A_D]
				if currentprice[i] > maxvalue[i]:
					maxvalue[i] = currentprice[i]
				if currentprice[i] < minvalue[i]:
					minvalue[i] = currentprice[i]
			print data
			update_realtime(data)

			if count%12==11:
				dt = datetime.now()
				for i in xrange(3):
					openvalue[i] = closevalue[i]
					closevalue[i] = currentprice[i]
					volume[i] = random.randint(100,1000)
					insert_history({stockid[i]:[dt,openvalue[i],closevalue[i],maxvalue[i],minvalue[i],volume[i]]})
					maxvalue[i] = 0
					minvalue[i] = 100
			count = count + 1
			sleep(0.1)