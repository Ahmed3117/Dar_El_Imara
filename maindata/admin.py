from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.template.context_processors import csrf
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.db.models import Sum

from inoutpay.models import MoneyWithDraw
from .models import IntermediaryTableWorkerCount,IntermediaryTableMarketCount,ExpectedProjectCosts,ProjectKhamatCosts, ProjectWorkersReserves, Project,inPay
from subdata.models import EmployeeCategory ,SubCategoryDetail,CategoryDetail
from userdata.models import Employee, MarketSources,User
from worksdata.models import DesignWork,EngSupervision
from django.template.loader import render_to_string
from finishcount.models import MarketCount, WorkerCount

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
            unpaid_ids = [project.id for project in queryset if project.totalcharge() > 0]
            return queryset.filter(id__in=unpaid_ids)
        if self.value() == 'notdepit':
            paid_ids = [project.id for project in queryset if project.totalcharge() <= 0]
            return queryset.filter(id__in=paid_ids)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_name': forms.Textarea(attrs={'rows':4}),
        }
class ExpectedProjectCostsAdmin(admin.ModelAdmin):
    list_display = ('project', 'main_category_detail', 'sub_category_detail', 'workers_reserves', 'workers_reserves_cost', 'khama', 'total_cost_for_this_khama')
    list_filter = ('project', 'main_category_detail', 'sub_category_detail')
    search_fields = ('project__project_name', 'main_category_detail__main_category', 'sub_category_detail__sub_category', 'workers__name', 'pay_reason', 'main_category_detail__main_category', 'market__sourcemarket')
    autocomplete_fields = ('project','khama')
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)

class ProjectKhamatCostsAdmin(admin.ModelAdmin):
    list_display = ('project', 'main_category_detail', 'sub_category_detail','who_paid','khama','market','total_cost_for_this_khama','paid','date_added')
    list_filter = ('project', 'main_category_detail', 'sub_category_detail')
    search_fields = ('project__project_name', 'main_category_detail__main_category', 'sub_category_detail__sub_category')
    autocomplete_fields = ('project','market','who_paid','khama')
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)

class ProjectWorkersReservesAdmin(admin.ModelAdmin):
    list_display = ('project', 'main_category_detail', 'sub_category_detail','date_added','worker','paid','charge')
    list_filter = ('project', 'main_category_detail', 'sub_category_detail','paid')
    search_fields = ('project__project_name', 'main_category_detail__main_category', 'sub_category_detail__sub_category')
    autocomplete_fields = ('project','worker')
    class Media:
        js = ('/static/admin/js/custom_project_costs.js',)

class DesignWorkInlineAdmin(admin.TabularInline):
    model = DesignWork
    extra = 0
    show_change_link = True
    # classes = ('collapse',)

class EngSupervisionInlineAdmin(admin.TabularInline):
    model = EngSupervision
    extra = 0
    show_change_link = True
    # classes = ('collapse',)

class ExpectedProjectCostsInlineAdmin(admin.TabularInline):
    model = ExpectedProjectCosts
    extra = 0
    show_change_link = True
    autocomplete_fields = ('khama',)
    # classes = ('collapse',)

class ProjectKhamatCostsInlineAdmin(admin.TabularInline):
    model = ProjectKhamatCosts
    extra = 0
    show_change_link = True
    # classes = ('collapse',)
    autocomplete_fields = ('market','who_paid','khama')

class ProjectWorkersReservesInlineAdmin(admin.TabularInline):
    model = ProjectWorkersReserves
    extra = 0
    show_change_link = True
    # autocomplete_fields = ('main_category_detail',)
    # classes = ('collapse',)

class inPayAdmin(admin.ModelAdmin):
    list_display = ('project', 'paid', 'giver', 'recipient', 'date_added')
    list_filter = ('project', )
    search_fields = ('project__project_name', 'giver__name', 'recipient__name', 'giver__code', 'recipient__code')
    autocomplete_fields = ('giver', 'recipient')

class InpayInlineAdmin(admin.TabularInline):
    model = inPay
    extra = 0
    show_change_link = True
    # classes = ('collapse',)
class MarketCountInlineAdmin(admin.TabularInline):
    model = MarketCount
    extra = 0
    show_change_link = True
    # classes = ('collapse',)
class IntermediaryTableMarketCountInlineAdmin(admin.TabularInline):
    model = IntermediaryTableMarketCount
    extra = 0
    max_num = 0
    # show_change_link = True
    # classes = ('collapse',)
class IntermediaryTableWorkerCountInlineAdmin(admin.TabularInline):
    model = IntermediaryTableWorkerCount
    extra = 0
    max_num = 0
    # show_change_link = True
    # classes = ('collapse',)

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    def has_add_permission(self, request):
        # if there's already an instance, do not allow adding
        if self.model.objects.count() > 15:
            return False
        return super().has_add_permission(request)
    # # to filter the project objects according to the current logginned user
    # # don't forget to add user field for 
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(user=request.user)
    # # to make user field of Project model to be the current logginned user as default
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.user = request.user
    #     super().save_model(request, obj, form, change)
    # def get_queryset(self, request):
    #     # Customize the queryset here
    #     # For example, let's say you want to only show objects with a specific attribute value
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.filter(is_done=False)
    #     return queryset

    list_display_links = ('project_name',)
    # list_display = ('is_done','project_name','client','projectinfo','totalprojectengsupervisioncosts','projecttotaldesignworkscosts','projectdeservedengsupervisioncosts','alldeservedmoney','totalinpaycosts','charge','designworksdetails','expectedprojectcosts','projectcosts','engsupervisionworksdetails','inpaydatails','printinvoice','date_added')
    list_display = ('is_done','project_name','client','details','printinvoice','coin','date_added')
    search_fields = ('client__name','client__code','project_name','project_address','coin__coin')
    list_filter = ('date_added','is_done',UnpaidFilter)
    inlines = [DesignWorkInlineAdmin,EngSupervisionInlineAdmin,ExpectedProjectCostsInlineAdmin,ProjectKhamatCostsInlineAdmin,ProjectWorkersReservesInlineAdmin,InpayInlineAdmin,IntermediaryTableWorkerCountInlineAdmin,IntermediaryTableMarketCountInlineAdmin]
    change_list_template = 'admin/maindata/Project/change_list.html'
    autocomplete_fields = ('client',)
    ordering = ('is_done','date_added')
    # class Media:
    #     js = ('/static/admin/js/custom_project_costs_inline.js',)
    # form = ClientForm
    # تفاصيل الشغلانات التابعة لهذا المشروع

    def details(self,obj):
        project_id = obj.id
        worksdata_designwork_changelist_url = reverse('admin:worksdata_designwork_changelist')
        worksdata_designwork_changelist_url += f'?project_id={project_id}'
        worksdata_engsupervision_changelist_url = reverse('admin:worksdata_engsupervision_changelist')
        worksdata_engsupervision_changelist_url += f'?project_id={project_id}'
        maindata_projectkhamatcosts_changelist_url = reverse('admin:maindata_projectkhamatcosts_changelist')
        maindata_projectkhamatcosts_changelist_url += f'?project_id={project_id}'
        maindata_projectworkersreserves_changelist_url = reverse('admin:maindata_projectworkersreserves_changelist')
        maindata_projectworkersreserves_changelist_url += f'?project_id={project_id}'
        maindata_expectedprojectcosts_changelist_url = reverse('admin:maindata_expectedprojectcosts_changelist')
        maindata_expectedprojectcosts_changelist_url += f'?project_id={project_id}'
        maindata_inpay_changelist_url = reverse('admin:maindata_inpay_changelist')
        maindata_inpay_changelist_url += f'?project_id={project_id}'
        modal_html = render_to_string('admin/maindata/Project/details.html', {
            'worksdata_designwork_changelist_url' : worksdata_designwork_changelist_url,
            'worksdata_engsupervision_changelist_url' : worksdata_engsupervision_changelist_url,
            'maindata_projectkhamatcosts_changelist_url' : maindata_projectkhamatcosts_changelist_url,
            'maindata_projectworkersreserves_changelist_url' : maindata_projectworkersreserves_changelist_url,
            'maindata_expectedprojectcosts_changelist_url' : maindata_expectedprojectcosts_changelist_url,
            'maindata_inpay_changelist_url' : maindata_inpay_changelist_url,
            'project_id' : project_id,
        })
        return format_html(modal_html)

    def designworksdetails(self, obj):
        project_id = obj.id
        url = reverse('admin:worksdata_designwork_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}"> اعمال التصميم </a>', url)

    # تفاصيل اعمال الاشراف الهندسى
    def engsupervisionworksdetails(self, obj):
        project_id = obj.id
        url = reverse('admin:worksdata_engsupervision_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}"> اعمال الاشراف  </a>', url)

    # تفاصيل  تكاليف الخامات
    def projectkhamatcosts(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_projectkhamatcosts_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">   تكاليف الخامات</a>', url)

    # تفاصيل  تكاليف الخامات
    def projectworkersreserves(self, obj):
        project_id = obj.id
        url = reverse('admin:maindata_projectworkersreserves_changelist')
        url += f'?project_id={project_id}'
        return format_html('<a class="button rounded " href="{}">   تكاليف المصنعيات</a>', url)

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

    

    designworksdetails.short_description = '  اعمال التصميم '
    projectkhamatcosts.short_description = 'تكاليف الخامات'
    projectworkersreserves.short_description = 'تكاليف المصنعيات'
    expectedprojectcosts.short_description = 'المصروفات المتوقعة'
    engsupervisionworksdetails.short_description = '  اعمال الاشراف  '
    inpaydatails.short_description = 'تفاصيل الوارد المالى '
    printinvoice.short_description = ' تقرير '
    showaddcostspage.short_description = ' اضف تكاليف '
    # projectinfo.short_description = '  معلومات المشروع '
    details.short_description = ' تفاصيل '

class OfficeCostsAdmin(admin.ModelAdmin):
    list_display = ('costtype', 'ammount', 'date_added', 'cost_reason', 'market', 'paid')
    list_filter = ('costtype', 'market')
    search_fields = ('cost_reason', 'market__sourcemarket')
    list_select_related = ('market',)

admin.site.register(inPay, inPayAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ExpectedProjectCosts, ExpectedProjectCostsAdmin)
admin.site.register(ProjectKhamatCosts, ProjectKhamatCostsAdmin)
admin.site.register(ProjectWorkersReserves, ProjectWorkersReservesAdmin)
# admin.site.register(OfficeCosts, OfficeCostsAdmin)
