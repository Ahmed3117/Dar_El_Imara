from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View

from finishcount.models import MarketCount, WorkerCount
from .models import ExpectedProjectCosts,ProjectKhamatCosts, ProjectWorkersReserves, Project,inPay
from subdata.models import EmployeeCategory ,SubCategoryDetail,CategoryDetail
from userdata.models import Employee, MarketSources,User
from worksdata.models import DesignWork,EngSupervision
from django.db.models import Sum
from admin_interface.models import Theme

def invoice(request, pk):
    obj = Project.objects.get(id = pk)
    #------------------------------------
    # التكاليف المتوقعة
    project_expected_costs_list = []
    project_expected_costs = ExpectedProjectCosts.objects.filter(project = obj).values('main_category_detail').annotate(total_workers_reserves = Sum('workers_reserves_cost'),total_khama = Sum('total_cost_for_this_khama'),total_sum = Sum('workers_reserves_cost') + Sum('total_cost_for_this_khama'))
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    print(project_expected_costs)
    for inst in project_expected_costs:
        obj_list = []
        main_category = CategoryDetail.objects.get(id = inst['main_category_detail']).main_category
        obj_list.append(main_category)
        obj_list.append(inst['total_workers_reserves'])
        obj_list.append(inst['total_khama'])
        obj_list.append(inst['total_sum'])
        project_expected_costs_list.append(obj_list)
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    #------------------------------------
    #  حساب اعمال التصميم
    designworks = DesignWork.objects.filter(project = obj)
    totaldesignworkscosts = 0
    for work in designworks :
        totaldesignworkscosts += work.workcost()
    #------------------------------------
    # حساب اعمال الاشراف              
    engsupervisionworks = EngSupervision.objects.filter(project = obj)
    totalengsupervisionworkscosts = 0
    for work in engsupervisionworks :
        totalengsupervisionworkscosts += work.workcost()
    #------------------------------------
    # تكاليف الخامات
    total_khamat_cost = 0
    khamat_costs = ProjectKhamatCosts.objects.filter(project = obj)
    for cost in khamat_costs:
        if cost.total_cost_for_this_khama:
            total_khamat_cost = total_khamat_cost + cost.total_cost_for_this_khama 
    #------------------------------------
    # تكاليف المصنعيات
    total_workersreserves_cost = 0
    workersreserves_costs = ProjectWorkersReserves.objects.filter(project = obj)
    for cost in workersreserves_costs:
        if cost.price:
            total_workersreserves_cost = total_workersreserves_cost + cost.price 
    #------------------------------------
    #الوارد المالى
    inpaycosts = inPay.objects.filter(project = obj)
    total_inpay_costs = 0
    for inpay in inpaycosts :
        total_inpay_costs += inpay.paid
    all_inpay_costs = total_inpay_costs
    # all_inpay_costs = total_inpay_costs + obj.paiddirectlybyclient()
    #------------------------------------
    # باقى الحساب
    # charge =0
    total_charge = all_inpay_costs - totaldesignworkscosts - totalengsupervisionworkscosts - total_khamat_cost - total_workersreserves_cost + obj.discount
    #------------------------------------
    client = obj.client
    #------------------------------------
    project_workersreserves = ProjectWorkersReserves.objects.filter(project = obj).values('worker').annotate(total_price = Sum('price'),total_paid = Sum('paid'))
    workersreserves = []
    for inst in project_workersreserves:
        worker_data = []
        charge = 0
        total_directly_paid = 0
        worker = User.objects.get(id = inst['worker'])
        worker_name = worker.name
        worker_code = worker.code
        worker_job = "غير معروف"
        try:
            worker_job = Employee.objects.get(user = worker).category.category
        except:
            pass
        directly_paid_costs = WorkerCount.objects.filter(project = obj,worker = worker)
        for cost in directly_paid_costs:
            if cost.directlyarrived:
                total_directly_paid = total_directly_paid + cost.directlyarrived 
                
        worker_data.append(worker.name)
        worker_data.append(worker_job)
        worker_data.append(inst['total_price'])
        all_paid = inst['total_paid'] + total_directly_paid
        worker_data.append(all_paid)
        worker_data.append(inst['total_price'] - all_paid)
        
        
        print(worker_data)
        workersreserves.append(worker_data)
    print(workersreserves)
    #-----------------------------------
    #----------------------------------------
    project_markets_reserves = ProjectKhamatCosts.objects.filter(project = obj).values('market').annotate(total_price = Sum('total_cost_for_this_khama'),total_paid = Sum('paid'))
    marketsreserves = []
    for inst in project_markets_reserves:
        market_data = []
        charge = 0
        total_directly_paid = 0
        if inst['market']:
            market = MarketSources.objects.get(id = inst['market'])
            directly_paid_costs = MarketCount.objects.filter(project = obj,source = market)
            for cost in directly_paid_costs:
                if cost.directlyarrived:
                    total_directly_paid = total_directly_paid + cost.directlyarrived 
            market_data.append(market.sourcemarket)
            market_data.append(inst['total_price'])
            all_paid = inst['total_paid'] + total_directly_paid
            market_data.append(all_paid)
            market_data.append(inst['total_price'] - all_paid)
            marketsreserves.append(market_data)
    #-----------------------------------
    
    theme = Theme.objects.get(active = 1)
    logo_url = None
    if theme.logo:
        logo = theme.logo
        logo_url = logo.url
    #-----------------------------------
    context = {
            'project_id' : pk,
            'project_expected_costs_list' : project_expected_costs_list,
            'totaldesignworkscosts' : totaldesignworkscosts,
            'totalengsupervisionworkscosts' : totalengsupervisionworkscosts,
            'total_khamat_cost' : total_khamat_cost,
            'total_workersreserves_cost' : total_workersreserves_cost,
            'all_inpay_costs' : all_inpay_costs,
            'total_charge' : total_charge,
            'workersreserves' : workersreserves,
            'marketsreserves' : marketsreserves,
            'inpaycosts' : inpaycosts,
            'designworks' : designworks,
            'engsupervisionworks' : engsupervisionworks,
            'client' : client,
            'logo_url' : logo_url,
        }
    return render(request,'maindata/invoice.html' ,context)
def addcostspage(request, pk):
    project = Project.objects.get(id = pk)
    main_categories = CategoryDetail.objects.all()
    context = {
        'project_pk':pk,
        'main_categories':main_categories,
        }
    return render(request,'maindata/project_costs.html' ,context)
def addmaincategory(request,project_pk):
    if request.method == 'POST':
        main_category = request.POST.get('tab1main_category')
        CategoryDetail.objects.create(main_category=main_category)
    return redirect('maindata:addcostspage' ,project_pk)
def addsubcategory(request,project_pk,main_category_pk):
    if request.method == 'POST':
        sub_category = request.POST.get('sub_category_'+str(main_category_pk))
        main_category = CategoryDetail.objects.get(id=main_category_pk)
        SubCategoryDetail.objects.create(main_category = main_category , sub_category = sub_category)
        
    return redirect('maindata:addcostspage' ,project_pk)
def addprojectcost(request,project_pk,main_category_pk,sub_category_pk):
    if request.method == 'POST':
        project = Project.objects.get(id=project_pk)
        main_category = CategoryDetail.objects.get(id=main_category_pk)
        sub_category = SubCategoryDetail.objects.get(id=sub_category_pk)
        workers_reserves = request.POST.get('workers_reserves', '')
        workers_reserves_cost = request.POST.get('workers_reserves_cost', '')
        khama = request.POST.get('khama', '')
        total_cost_for_this_khama = request.POST.get('total_cost_for_this_khama', '')
        expectedcost = ExpectedProjectCosts.objects.create(project=project,main_category_detail = main_category,sub_category_detail = sub_category,workers_reserves = workers_reserves , workers_reserves_cost = workers_reserves_cost,khama = khama,total_cost_for_this_khama=total_cost_for_this_khama)
        expectedcost.save()
        serialized_expected_costs = []
        serialized_expected_costs = [expectedcost]
        expectedcost = serializers.serialize('json', serialized_expected_costs, fields=('workers_reserves', 'workers_reserves_cost', 'khama', 'total_cost_for_this_khama'))
    
    return JsonResponse({'expectedcost': expectedcost}, safe=False)       
def get_project_expected_costs(request,subcategory_id):
    # sub_category_detail
    subcategory = SubCategoryDetail.objects.get(id = subcategory_id)
    costs = ExpectedProjectCosts.objects.filter(sub_category_detail=subcategory)
    costs_json = serializers.serialize('json', costs, fields=('workers_reserves', 'workers_reserves_cost', 'khama', 'total_cost_for_this_khama'))
    return JsonResponse(costs_json, safe=False)



















#---------------------------------------------------------
# views to customize projectcosts of admin panel
class GetCategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_type = request.GET.get('category_type', 'T')
        categories = EmployeeCategory.objects.filter(category_type=category_type).values('id', 'category')
        return JsonResponse(list(categories), safe=False)

class GetCategoryWorkers(View):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        employee_category = EmployeeCategory.objects.get(id = category)
        workers = Employee.objects.filter(category=employee_category).values('id', 'name')
        return JsonResponse(list(workers), safe=False)

class GetCategorySubs(View):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        # employee_category = EmployeeCategory.objects.get(id = category)
        subs = SubCategoryDetail.objects.filter(main_category=category).values('id', 'sub_category')
        print("ssssssssssssssssssssssssssssss")
        print(subs)
        return JsonResponse(list(subs), safe=False)

# class GetProjectWorkersdata(View):
#     def get(self, request, *args, **kwargs):
#         worker_id = request.GET.get('worker_id')
#         project_id = request.GET.get('project_id')
#         project = Project.objects.get(id = project_id)
#         worker = Employee.objects.get(id = worker_id)
#         worker_reserves = ProjectWorkersReserves.objects.filter(project=project,worker =worker).values('id', 'name').group_by(paid)
#         return JsonResponse(list(workers), safe=False)