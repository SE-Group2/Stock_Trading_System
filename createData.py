from search.models import StockHistoryInfo
from database.models import StockInfo

from datetime import datetime
import random


x = StockInfo(StockID="111111",StockName="baidu",CurrentPrice=10.3,A_D=0.2,UpLimit=100,DownLimit=1)
x.save()
x = StockInfo(StockID="222222",StockName="alipp",CurrentPrice=11.3,A_D=0.3,UpLimit=100,DownLimit=1)
x.save()
x = StockInfo(StockID="333333",StockName="qq",CurrentPrice=12.3,A_D=0.1,UpLimit=100,DownLimit=1)
x.save()

dt = datetime.now()


a = random.random()*10+5
b = random.random()*10+5
c = random.random()*10+5
d = random.random()*10+5
for i in xrange(1,20):
	a = b
	b = random.random()*10+5
	c = random.random()*10+5
	d = random.random()*10+5
	dt = dt.replace(hour=i/60,minute=i%60)
	x = StockHistoryInfo(StockID=StockInfo.objects.get(StockID="111111"),HistoryTime=dt,Open_value=a,Close_value=b,Highest_value=max(a,b,c,d),Lowest_value=min(a,b,c,d),Volume_value=1000,EMA12=0,EMA26=0,DIF=0,MACD=0)
	x.save()

for i in xrange(1,20):
	a = b
	b = random.random()*10+5
	c = random.random()*10+5
	d = random.random()*10+5
	dt = dt.replace(hour=i/60,minute=i%60)
	x = StockHistoryInfo(StockID=StockInfo.objects.get(StockID="222222"),HistoryTime=dt,Open_value=a,Close_value=b,Highest_value=max(a,b,c,d),Lowest_value=min(a,b,c,d),Volume_value=1000,EMA12=0,EMA26=0,DIF=0,MACD=0)
	x.save()

for i in xrange(1,20):
	a = b
	b = random.random()*10+5
	c = random.random()*10+5
	d = random.random()*10+5
	dt = dt.replace(hour=i/60,minute=i%60)
	x = StockHistoryInfo(StockID=StockInfo.objects.get(StockID="333333"),HistoryTime=dt,Open_value=a,Close_value=b,Highest_value=max(a,b,c,d),Lowest_value=min(a,b,c,d),Volume_value=1000,EMA12=0,EMA26=0,DIF=0,MACD=0)
	x.save()