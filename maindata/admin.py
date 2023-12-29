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
        modal_html = render_to_string('admin/maindata/project/details.html', {
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

    # def projectinfo(self, obj):
    #     project_id = obj.id
    #     #------------------------------------
    #     #  حساب اعمال التصميم
    #     designworks = DesignWork.objects.filter(project = obj)
    #     totaldesignworkscosts = 0
    #     for work in designworks :
    #         totaldesignworkscosts += work.workcost()
    #     #------------------------------------
    #     # حساب اعمال الاشراف
    #     engsupervisionworks = EngSupervision.objects.filter(project = obj)
    #     totalengsupervisionworkscosts = 0
    #     for work in engsupervisionworks :
    #         totalengsupervisionworkscosts += work.workcost()
    #     #------------------------------------
    #     # تكاليف الخامات
    #     total_khamat_cost = 0
    #     khamat_costs = ProjectKhamatCosts.objects.filter(project = obj)
    #     for cost in khamat_costs:
    #         if cost.total_cost_for_this_khama:
    #             total_khamat_cost = total_khamat_cost + cost.total_cost_for_this_khama
    #     #------------------------------------
    #     # تكاليف المصنعيات
    #     total_workersreserves_cost = 0
    #     workersreserves_costs = ProjectWorkersReserves.objects.filter(project = obj)
    #     for cost in workersreserves_costs:
    #         if cost.price:
    #             total_workersreserves_cost = total_workersreserves_cost + cost.price
    #     #------------------------------------
    #     #الوارد المالى
    #     inpaycosts = inPay.objects.filter(project = obj)
    #     total_inpay_costs = 0
    #     for inpay in inpaycosts :
    #         total_inpay_costs += inpay.paid
    #     all_inpay_costs = total_inpay_costs
    #     # all_inpay_costs = total_inpay_costs + obj.paiddirectlybyclient()
    #     #------------------------------------
    #     # باقى الحساب
    #     # charge =0
    #     total_charge = all_inpay_costs - totaldesignworkscosts - totalengsupervisionworkscosts - total_khamat_cost - total_workersreserves_cost + obj.discount
    #     #------------------------------------
    #     #########################################################################################
    #     #########################################################################################
    #     #------------------------------------
    #     # تكاليف دفعها العميل
    #     # paid_by_client = ProjectCosts.objects.filter(project = self , who_paid = 'c')
    #     # total_paid_by_client = 0
    #     # for paid in paid_by_client :
    #     #     total_paid_by_client += paid.ammount
    #     #----------------------------------------
    #     project_workersreserves = ProjectWorkersReserves.objects.filter(project = obj).values('worker').annotate(total_price = Sum('price'),total_paid = Sum('paid'))
    #     workersreserves = []
    #     for inst in project_workersreserves:
    #         worker_data = []
    #         charge = 0
    #         total_directly_paid = 0
    #         worker = User.objects.get(id = inst['worker'])
    #         worker_job = Employee.objects.get(user = worker).category.category
    #         directly_paid_costs = WorkerCount.objects.filter(project = obj,worker = worker)
    #         for cost in directly_paid_costs:
    #             if cost.directlyarrived:
    #                 total_directly_paid = total_directly_paid + cost.directlyarrived
    #         worker_data.append(worker.name)
    #         worker_data.append(worker_job)
    #         worker_data.append(inst['total_price'])
    #         all_paid = inst['total_paid'] + total_directly_paid
    #         worker_data.append(all_paid)
    #         worker_data.append(inst['total_price'] - all_paid)
    #         workersreserves.append(worker_data)
    #     #----------------------------------------
    #     project_markets_reserves = ProjectKhamatCosts.objects.filter(project = obj).values('market').annotate(total_price = Sum('total_cost_for_this_khama'),total_paid = Sum('paid'))
    #     marketsreserves = []
    #     for inst in project_markets_reserves:
    #         market_data = []
    #         charge = 0
    #         total_directly_paid = 0
    #         if inst['market']:
    #             market = MarketSources.objects.get(id = inst['market'])
    #             directly_paid_costs = MarketCount.objects.filter(project = obj,source = market)
    #             for cost in directly_paid_costs:
    #                 if cost.directlyarrived:
    #                     total_directly_paid = total_directly_paid + cost.directlyarrived
    #             market_data.append(market.sourcemarket)
    #             market_data.append(inst['total_price'])
    #             all_paid = inst['total_paid'] + total_directly_paid
    #             market_data.append(all_paid)
    #             market_data.append(inst['total_price'] - all_paid)
    #             marketsreserves.append(market_data)

    #     modal_html = render_to_string('admin/maindata/project/projectinfo.html', {
    #         'project_id' : project_id,
    #         'totaldesignworkscosts' : totaldesignworkscosts,
    #         'totalengsupervisionworkscosts' : totalengsupervisionworkscosts,
    #         'total_khamat_cost' : total_khamat_cost,
    #         'total_workersreserves_cost' : total_workersreserves_cost,
    #         'all_inpay_costs' : all_inpay_costs,
    #         'total_charge' : total_charge,
    #         'workersreserves' : workersreserves,
    #         'marketsreserves' : marketsreserves,
    #     })
    #     return format_html(modal_html)

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
