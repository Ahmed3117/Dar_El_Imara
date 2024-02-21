from django.contrib import admin
from .models import  MoneyWithDraw
from maindata.models import Coin
# Register your models here.

class MoneyWithDrawAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'ammount', 'date_added', 'pay_reason')
    list_filter = ('project', 'user','date_added')
    search_fields = ('project__project_name', 'user__name', 'pay_reason')

class CoinAdmin(admin.ModelAdmin):
    list_display = ('coin','ammount_in_egyption_pound','date_updated')
    search_fields = ('coin', )


admin.site.register(MoneyWithDraw, MoneyWithDrawAdmin)
admin.site.register(Coin, CoinAdmin)