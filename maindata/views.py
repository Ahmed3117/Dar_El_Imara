from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from .models import EmployeeCategory, ExpectedProjectCosts,Project,Employee, ProjectCosts,SubCategoryDetail,CategoryDetail
def invoice(request, pk):
    context = {
        # 'main_categories':main_categories,
        # 'paid_monthes':paid_monthes,
        # 'sellprocesses':sellprocesses,
        # 'supposed_paid_month':supposed_paid_month,
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
        build_subjects = request.POST.get('build_subjects', '')
        build_subjects_cost = request.POST.get('build_subjects_cost', '')
        expectedcost = ExpectedProjectCosts.objects.create(project=project,main_category_detail = main_category,sub_category_detail = sub_category,workers_reserves = workers_reserves , workers_reserves_cost = workers_reserves_cost,build_subjects = build_subjects,build_subjects_cost=build_subjects_cost)
        expectedcost.save()
        serialized_expected_costs = []
        serialized_expected_costs = [expectedcost]
        expectedcost = serializers.serialize('json', serialized_expected_costs, fields=('workers_reserves', 'workers_reserves_cost', 'build_subjects', 'build_subjects_cost'))
    
    return JsonResponse({'expectedcost': expectedcost}, safe=False)
        

def get_project_expected_costs(request,subcategory_id):
    # sub_category_detail
    subcategory = SubCategoryDetail.objects.get(id = subcategory_id)
    costs = ExpectedProjectCosts.objects.filter(sub_category_detail=subcategory)
    costs_json = serializers.serialize('json', costs, fields=('workers_reserves', 'workers_reserves_cost', 'build_subjects', 'build_subjects_cost'))
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