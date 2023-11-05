
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views import View
from .models import EmployeeCategory,Project
def invoice(request, pk):
    project = Project.objects.get(id = pk)
    
    context = {
        # 'pill':pill,
        # 'paid_monthes':paid_monthes,
        # 'sellprocesses':sellprocesses,
        # 'supposed_paid_month':supposed_paid_month,
        }
    return render(request,'maindata/invoice.html' ,context)



class GetCategoriesView(View):
    def get(self, request, *args, **kwargs):
        category_type = request.GET.get('category_type', 'T')
        categories = EmployeeCategory.objects.filter(category_type=category_type).values('id', 'category')
        return JsonResponse(list(categories), safe=False)