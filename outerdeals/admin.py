from django.contrib import admin
from .models import OfficeCosts
# Register your models here.

class OfficeCostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'ammount', 'date_added', 'cost_reason', 'file')
    autocomplete_fields = ('user',)
    
admin.site.register(OfficeCosts,OfficeCostsAdmin)