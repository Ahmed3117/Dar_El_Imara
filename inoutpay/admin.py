from django.contrib import admin
from .models import MoneyWithDraw
# Register your models here.

class MoneyWithDrawAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'ammount', 'date_added', 'pay_reason')
    list_filter = ('project', 'user','date_added')
    search_fields = ('project__project_name', 'user__name', 'pay_reason')


admin.site.register(MoneyWithDraw, MoneyWithDrawAdmin)