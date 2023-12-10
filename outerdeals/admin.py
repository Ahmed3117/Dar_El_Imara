from django.contrib import admin
from .models import MonthPay, OfficeCosts, OutDeals
from django.utils.translation import gettext_lazy as _

class UnpaidFilter(admin.SimpleListFilter):
    title = _(' المديونيات')
    parameter_name = 'FinishedORNot'

    def lookups(self, request, model_admin):
        return (
            ('depit', _('المديونين')),
            ('notdepit', _('الغير مديونين')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'depit':
            unpaid_ids = [outdeal.id for outdeal in queryset if outdeal.charge() > 0]
            return queryset.filter(id__in=unpaid_ids)
        if self.value() == 'notdepit':
            paid_ids = [outdeal.id for outdeal in queryset if outdeal.charge() <= 0]
            return queryset.filter(id__in=paid_ids)





class OfficeCostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'ammount', 'date_added', 'cost_reason', 'file')
    autocomplete_fields = ('user',)
    
class MonthPayInlineAdmin(admin.TabularInline):
    model = MonthPay
    extra = 1
    show_change_link = True
    # classes = ('collapse',)


    
class OutDealsAdmin(admin.ModelAdmin):
    list_display = ('creditor','debtor','ammount','paid','charge','file','date_added')
    search_fields = ('creditor__name','debtor_name','reason')
    list_filter = ('date_added','creditor','debtor',UnpaidFilter)
    inlines = [MonthPayInlineAdmin,]
    autocomplete_fields = ('creditor','debtor')    
    
    

admin.site.register(OfficeCosts,OfficeCostsAdmin)
admin.site.register(OutDeals,OutDealsAdmin)