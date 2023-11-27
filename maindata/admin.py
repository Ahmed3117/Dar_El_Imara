from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.template.context_processors import csrf
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from .forms import EmployeeForm
from .models import CategoryDetail, ExpectedProjectCosts, ProjectKhamatCosts,SubCategoryDetail, DesignWorkType, EmployeeCategory, Client, Employee, DesignWork, EngSupervision, ProjectCosts, Project, inPay, MoneyWithDraw, OfficeCosts, MarketSources
from django.template.loader import render_to_string



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

class SubCategoryDetailInlineAdmin(admin.TabularInline):
    model = SubCategoryDetail
    extra = 1
    show_change_link = True
    # classes = ('collapse',)
    
class CategoryDetailAdmin(admin.ModelAdmin):
    list_display = ('main_category',)
    search_fields = ('main_category',)
    inlines = [SubCategoryDetailInlineAdmin]

class SubCategoryDetailAdmin(admin.ModelAdmin):
    list_display = ('sub_category','main_category')
    search_fields = ('sub_category','main_category')
    list_filter = ('main_category',)

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
    search_fields = ('project__project_name', 'client__name', 'engineers__name', 'workers__name', 'pay_reason', 'main_category_detail__main_category', 'market__sourcemarket')
    list_select_related = ('project', 'client', 'engineers', 'workers', 'main_category_detail', 'market')
    autocomplete_fields = ('project',)
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)
class ExpectedProjectCostsAdmin(admin.ModelAdmin):
    list_display = ('project', 'main_category_detail', 'sub_category_detail', 'workers_reserves', 'workers_reserves_cost', 'build_subjects', 'build_subjects_cost')
    list_filter = ('project', 'main_category_detail', 'sub_category_detail')
    search_fields = ('project__project_name', 'main_category_detail__main_category', 'sub_category_detail__sub_category', 'workers__name', 'pay_reason', 'main_category_detail__main_category', 'market__sourcemarket')
    autocomplete_fields = ('project',)
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)
    
class ProjectKhamatCostsAdmin(admin.ModelAdmin):
    list_display = ('project', 'main_category_detail', 'sub_category_detail','date_added')
    list_filter = ('project', 'main_category_detail', 'sub_category_detail')
    search_fields = ('project__project_name', 'main_category_detail__main_category', 'sub_category_detail__sub_category')
    autocomplete_fields = ('project',)
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
    extra = 3
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
class ExpectedProjectCostsInlineAdmin(admin.TabularInline):
    model = ExpectedProjectCosts
    extra = 0
    show_change_link = True
class ProjectKhamatCostsInlineAdmin(admin.TabularInline):
    model = ProjectKhamatCosts
    extra = 0
    show_change_link = True

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
    
    list_display_links = ('project_name',)
    # list_display = ('is_done','project_name','client','projectinfo','totalprojectengsupervisioncosts','projecttotaldesignworkscosts','projectdeservedengsupervisioncosts','alldeservedmoney','totalinpaycosts','charge','designworksdetails','expectedprojectcosts','projectcosts','engsupervisionworksdetails','inpaydatails','printinvoice','date_added')
    list_display = ('is_done','project_name','client','projectinfo','designworksdetails','expectedprojectcosts','projectcosts','engsupervisionworksdetails','inpaydatails','printinvoice','date_added')
    search_fields = ('client__name','project_name','project_address')
    list_filter = ('date_added','is_done',UnpaidFilter)

    inlines = [DesignWorkInlineAdmin,EngSupervisionInlineAdmin,ExpectedProjectCostsInlineAdmin,ProjectKhamatCostsInlineAdmin,InpayInlineAdmin]
    change_list_template = 'admin/maindata/Project/change_list.html'
    # class Media:
    #     js = ('/static/admin/js/custom_project_costs_inline.js',)
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
        return format_html('<a class="button rounded " href="{}"> اعمال الاشراف  </a>', url)
    
    # تفاصيل مصروفات المشروع
    def projectcosts(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_projectcosts_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">  المصروفات الفعلية</a>', url)
    
    def expectedprojectcosts(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_expectedprojectcosts_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">   المصروفات المتوقعة</a>', url)
    
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
    # add costs
    def showaddcostspage(self, obj):
        project_id = obj.id
        url = reverse('maindata:addcostspage', args=[project_id])
        return format_html('<a class="button rounded " href="{}">اضف تكاليف </a>', url)

    def projectinfo(self, obj):
        project_id = obj.id
        #------------------------------------
        #  حساب اعمال التصميم
        designworks = DesignWork.objects.filter(project = obj)
        totaldesignworkscosts = 0
        for work in designworks :
            totaldesignworkscosts += work.work_cost
        #------------------------------------
        # تكاليف دفعها العميل
        # paid_by_client = ProjectCosts.objects.filter(project = self , who_paid = 'c')
        # total_paid_by_client = 0
        # for paid in paid_by_client :
        #     total_paid_by_client += paid.ammount
        #------------------------------------
        # حساب اعمال الاشراف 
        engsupervisionworks = EngSupervision.objects.filter(project = obj)
        totalengsupervisionworkscosts = 0
        for work in engsupervisionworks :
            totalengsupervisionworkscosts += work.work_cost
        #------------------------------------
        # تكاليف المشروع
        total_work_cost = 0
        work_costs = ProjectCosts.objects.filter(project = obj)
        for cost in work_costs:
            if cost.ammount:
                total_work_cost = total_work_cost + cost.ammount 
        #------------------------------------
        #الوارد المالى
        inpaycosts = inPay.objects.filter(project = obj)
        total_inpay_costs = 0
        for inpay in inpaycosts :
            total_inpay_costs += inpay.paid
        all_inpay_costs = total_inpay_costs + obj.paiddirectlybyclient()
        #------------------------------------
        # باقى الحساب
        charge = obj.totalinpaycosts() - obj.alldeservedmoney() -obj.totalprojectengsupervisioncosts() + obj.discount

        #------------------------------------
        modal_html = render_to_string('admin/maindata/project/projectinfo.html', {
            'project_id' : project_id,
            'totaldesignworkscosts' : totaldesignworkscosts,
            'totalengsupervisionworkscosts' : totalengsupervisionworkscosts,
            'total_work_cost' : total_work_cost,
            'all_inpay_costs' : all_inpay_costs,
            'charge' : int(charge),
        })
        return format_html(modal_html)
    designworksdetails.short_description = '  اعمال التصميم '
    projectcosts.short_description = 'المصروفات الفعلية'
    expectedprojectcosts.short_description = 'المصروفات المتوقعة'
    engsupervisionworksdetails.short_description = '  اعمال الاشراف  '
    inpaydatails.short_description = 'تفاصيل الوارد المالى '
    printinvoice.short_description = ' تقرير '
    showaddcostspage.short_description = ' اضف تكاليف '
    projectinfo.short_description = '  معلومات المشروع '


class MoneyWithDrawAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'ammount', 'date_added', 'pay_reason')
    list_filter = ('project', 'user','date_added')
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
# admin.site.register(SubCategoryDetail, SubCategoryDetailAdmin)
admin.site.register(DesignWorkType, DesignWorkTypeAdmin)
admin.site.register(EmployeeCategory, EmployeeCategoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DesignWork, DesignWorkAdmin)
admin.site.register(EngSupervision, EngSupervisionAdmin)
admin.site.register(ProjectCosts, ProjectCostsAdmin)
admin.site.register(ExpectedProjectCosts, ExpectedProjectCostsAdmin)
admin.site.register(ProjectKhamatCosts, ProjectKhamatCostsAdmin)
admin.site.register(inPay, inPayAdmin)
admin.site.register(MoneyWithDraw, MoneyWithDrawAdmin)
admin.site.register(OfficeCosts, OfficeCostsAdmin)
admin.site.register(MarketSources, MarketSourcesAdmin)


