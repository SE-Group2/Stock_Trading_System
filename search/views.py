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
import json
import random

# Create your views here.

HasOpened = False


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
		except StockInfo.DoesNotExist:
			pass
	else:
		pk = random.randint(1,StockInfo.objects.count())
		try:
			x = StockInfo.objects.get(pk=pk)
		except StockInfo.DoesNotExist:
			pass
	return render(req,'stock.html',{"stockid":x.StockID,"stockname":x.StockName,"data":json.dumps(JsonResp(x))})


def JsonResp(x):
	list = []
	try:
		historyinfo = StockHistoryInfo.objects.filter(StockID=x).order_by('-HistoryTime')[:20]
	except StockHistoryInfo.DoesNotExist:
		pass
	else:
		for i in historyinfo:
			s = i.HistoryTime.strftime("%a %b %d %H:%M:%S +0800 %Y")
			x = {"volume":i.Volume_value,"open":i.Open_value,"high":i.Highest_value,"close":i.Close_value,"low":i.Lowest_value,"time":s}
			list.append(x)
		data = {"symbol":"SHxxxxx","name":"aaaa","list":list}
		return data


def refresh_5s(req):
	if req.method == 'POST':
		stockinfo = req.POST.get('value')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
		except StockInfo.DoesNotExist:
			pass
		else:
			return JsonResponse({'result':1,'StockID':x.StockID,'CurrentPrice':x.CurrentPrice})
	else:
		res = {}
		res["result"] = 0
		return JsonResponse(res)


def refresh_1min(req):
	if req.method == 'POST':
		stockinfo = req.POST.get('value')
		try:
			x = StockInfo.objects.get(Q(StockID=stockinfo)|Q(StockName=stockinfo))
			historyinfo = StockHistoryInfo.objects.filter(StockID=x.StockID).order_by('-HistoryTime')[:20]
		except StockInfo.DoesNotExist:
			pass
		except StockHistoryInfo.DoesNotExist:
			pass
		else:
			return JsonResponse({"result":1,"data":JsonResp(historyinfo)})
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