from django.contrib import admin
from .models import StockInfo,StockHistoryInfo

# Register your models here.
admin.site.register(StockInfo)
admin.site.register(StockHistoryInfo)