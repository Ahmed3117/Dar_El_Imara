from django.contrib import admin
from .models import DesignWorkType,DesignWork,EngSupervision

class DesignWorkTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'unit_price','mitr_price')
    list_filter = ('type',)
    search_fields = ('type',)

class DesignWorkAdmin(admin.ModelAdmin):
    list_display = ('project', 'worktype', 'account_way', 'ammount', 'date_added', 'work_cost')
    list_filter = ('project', 'account_way', 'worktype')
    search_fields = ('project__project_name', 'worktype__type')
    list_select_related = ('project', 'worktype')
    
class EngSupervisionAdmin(admin.ModelAdmin):
    list_display = ('project', 'account_way', 'ammount', 'date_added', 'all_costs', 'work_cost')
    list_filter = ('project', 'account_way')
    search_fields = ('project__project_name','project__client__name')
    # list_select_related = ('project',)
    readonly_fields = ('work_cost',)

admin.site.register(DesignWorkType, DesignWorkTypeAdmin)
admin.site.register(DesignWork, DesignWorkAdmin)
admin.site.register(EngSupervision, EngSupervisionAdmin)