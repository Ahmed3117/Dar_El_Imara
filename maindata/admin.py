from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.template.context_processors import csrf
from django.utils.translation import gettext_lazy as _

from .forms import EmployeeForm
from .models import CategoryDetail, DesignWorkType, EmployeeCategory, Client, Employee, DesignWork, EngSupervision, ProjectCosts, Project, inPay, OutPay, OfficeCosts, MarketSources
# from .forms import ClientForm



class UnpaidFilter(admin.SimpleListFilter):
    title = _('كشف المديونيات')
    parameter_name = 'FinishedORNot'

    def lookups(self, request, model_admin):
        return (
            ('depit', _('المديونين')),
            ('notdepit', _('الغير مديونين')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'depit':
            unpaid_ids = [project.id for project in queryset if project.charge() > 0]
            return queryset.filter(id__in=unpaid_ids)
        if self.value() == 'notdepit':
            paid_ids = [project.id for project in queryset if project.charge() <= 0]
            return queryset.filter(id__in=paid_ids)

class CategoryDetailAdmin(admin.ModelAdmin):
    list_display = ('pay_category',)
    search_fields = ('pay_category',)

class DesignWorkTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'unit_price', 'mitr_price')
    list_filter = ('type',)
    search_fields = ('type',)

class EmployeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'category_type')
    list_filter = ('category_type',)
    search_fields = ('category',)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_id', 'phone_number', 'address', 'code')
    search_fields = ('name', 'national_id', 'phone_number', 'address', 'code')

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ('name', 'type', 'category')
    list_filter = ('type', 'category')
    search_fields = ('name', 'type', 'category')
    class Media:
        js = ('/static/admin/js/employee_types.js',)
    
class DesignWorkAdmin(admin.ModelAdmin):
    list_display = ('project', 'worktype', 'account_way', 'ammount', 'date_added', 'work_cost')
    list_filter = ('project', 'account_way', 'worktype')
    search_fields = ('project__project_name', 'worktype__type')
    list_select_related = ('project', 'worktype')

class EngSupervisionAdmin(admin.ModelAdmin):
    list_display = ('project', 'account_way', 'ammount', 'date_added', 'all_costs', 'work_cost')
    list_filter = ('project', 'account_way')
    search_fields = ('project__project_name',)
    # list_select_related = ('project',)

class ProjectCostsAdmin(admin.ModelAdmin):
    list_display = ('project', 'ammount', 'who_paid', 'get_name_of_paid_person', 'pay_reason', 'pay_reason_category', 'get_name_of_pay_reason_category')
    list_filter = ('project', 'who_paid', 'pay_reason_category')
    search_fields = ('project__project_name', 'client__name', 'engineers__name', 'workers__name', 'pay_reason', 'pay_category_detail__pay_category', 'market__sourcemarket')
    list_select_related = ('project', 'client', 'engineers', 'workers', 'pay_category_detail', 'market')
    
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)
class inPayAdmin(admin.ModelAdmin):
    list_display = ('project', 'paid', 'giver', 'recipient', 'date_added')
    list_filter = ('project', 'giver', 'recipient')
    search_fields = ('project__project_name', 'giver', 'recipient')


class DesignWorkInlineAdmin(admin.TabularInline):
    model = DesignWork
    extra = 1
    show_change_link = True
    # classes = ('collapse',)
class EngSupervisionInlineAdmin(admin.TabularInline):
    model = EngSupervision
    extra = 1
    show_change_link = True
    # classes = ('collapse',)
class ProjectCostsInlineAdmin(admin.TabularInline):
    model = ProjectCosts
    extra = 1
    show_change_link = True
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        
        # Add placeholders for specific fields
        if db_field.name == 'who_paid':
            field.widget.attrs['placeholder'] = 'القائم بالدفع'
        elif db_field.name == 'ammount':
            field.widget.attrs['placeholder'] = 'القيمة'
        elif db_field.name == 'pay_reason':
            field.widget.attrs['placeholder'] = 'سبب الصرف'
        elif db_field.name == 'workers':
            field.widget.attrs['placeholder'] = ' العامل'

        # Add more fields and their placeholders as needed

        return field
class InpayInlineAdmin(admin.TabularInline):
    model = inPay
    extra = 1
    show_change_link = True
    # classes = ('collapse',)
    
class ProjectAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     # Customize the queryset here
    #     # For example, let's say you want to only show objects with a specific attribute value
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.filter(is_done=False)
    #     return queryset
    list_display = ('is_done','project_name','project_address','client','date_added','totalprojectengsupervisioncosts','projecttotaldesignworkscosts','projectdeservedengsupervisioncosts','alldeservedmoney','totalinpaycosts','charge','designworksdetails','projectcosts','engsupervisionworksdetails','inpaydatails','printinvoice')
    search_fields = ('client__name','project_name','project_address')
    list_filter = ('date_added','is_done',UnpaidFilter)
    inlines = [DesignWorkInlineAdmin,EngSupervisionInlineAdmin,ProjectCostsInlineAdmin,InpayInlineAdmin]
    change_list_template = 'admin/maindata/Project/change_list.html'
    class Media:
        js = ('/static/admin/js/custom_project_costs_inline.js',)
    # form = ClientForm
    # تفاصيل الشغلانات التابعة لهذا المشروع
    def designworksdetails(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_designwork_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}"> اعمال التصميم </a>', url)
    
    # تفاصيل اعمال الاشراف الهندسى
    def engsupervisionworksdetails(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_engsupervision_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}"> اعمال الاشراف الهندسى </a>', url)
    
    # تفاصيل مصروفات المشروع
    def projectcosts(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_projectcosts_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">    مصروفات المشروع</a>', url)
    
    # تفاصيل الوارد المالى
    def inpaydatails(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_inpay_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">  الوارد المالى</a>', url)
    
    # report
    def printinvoice(self, obj):
        project_id = obj.id
        url = reverse('maindata:invoice', args=[project_id])
        return format_html('<a class="button rounded " href="{}">تقرير </a>', url)

    designworksdetails.short_description = ' تفاصيل اعمال التصميم '
    projectcosts.short_description = 'تفاصيل مصروفات المشروع '
    engsupervisionworksdetails.short_description = 'تفاصيل  اعمال الاشراف الهندسى '
    inpaydatails.short_description = 'تفاصيل الوارد المالى '
    printinvoice.short_description = ' تقرير '


class OutPayAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'ammount', 'date_added', 'pay_reason')
    list_filter = ('project', 'user')
    search_fields = ('project__project_name', 'user__name', 'pay_reason')

class OfficeCostsAdmin(admin.ModelAdmin):
    list_display = ('costtype', 'ammount', 'date_added', 'cost_reason', 'market', 'paid')
    list_filter = ('costtype', 'market')
    search_fields = ('cost_reason', 'market__sourcemarket')
    list_select_related = ('market',)

class MarketSourcesAdmin(admin.ModelAdmin):
    list_display = ('sourcemarket', 'phone_number', 'address')
    search_fields = ('sourcemarket', 'phone_number', 'address')

# Register your models with the admin site
admin.site.register(Project,ProjectAdmin)
admin.site.register(CategoryDetail, CategoryDetailAdmin)
admin.site.register(DesignWorkType, DesignWorkTypeAdmin)
admin.site.register(EmployeeCategory, EmployeeCategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DesignWork, DesignWorkAdmin)
admin.site.register(EngSupervision, EngSupervisionAdmin)
admin.site.register(ProjectCosts, ProjectCostsAdmin)
admin.site.register(inPay, inPayAdmin)
admin.site.register(OutPay, OutPayAdmin)
admin.site.register(OfficeCosts, OfficeCostsAdmin)
admin.site.register(MarketSources, MarketSourcesAdmin)

