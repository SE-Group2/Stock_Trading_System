from django.contrib import admin
from .models import StockHistoryInfo, StockInfo

# Register your models here.
admin.site.register(StockHistoryInfo)
admin.site.register(StockInfo)
