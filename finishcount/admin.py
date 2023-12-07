from django.contrib import admin

from finishcount.models import MarketCount, WorkerCount

# Register your models here.
class MarketCountAdmin(admin.ModelAdmin):
    list_display = ('project', 'source', 'directlyarrived', 'date_added', 'file','deservedforthisproject','alreadypaidforthisproject','charge')
    list_filter = ('project', )
    search_fields = ('project__project_name', 'source__sourcemarket', 'source__phone_number')
    autocomplete_fields = ('project', 'source')
    
class WorkerCountAdmin(admin.ModelAdmin):
    list_display = ('project', 'worker', 'directlyarrived', 'date_added', 'file','deservedforthisproject','alreadypaidforthisproject','charge')
    list_filter = ('project', )
    search_fields = ('project__project_name', 'worker__name', 'worker__phone_number')
    autocomplete_fields = ('project', 'worker')


admin.site.register(MarketCount, MarketCountAdmin)
admin.site.register(WorkerCount,WorkerCountAdmin)