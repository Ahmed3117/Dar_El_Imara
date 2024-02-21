from django.contrib import admin
from django.urls import include, path
from .views import GetCategoriesView,GetCategoryWorkers,addmaincategory, addprojectcost, addsubcategory, get_project_expected_costs,gettotaldata, invoice,GetCategorySubs,addcostspage,showfullreport,fullreport,getselectedclientaddress
app_name = 'maindata'

urlpatterns = [
    path('invoice/<int:pk>/', invoice, name="invoice"),
    path('addcosts/<int:pk>/', addcostspage, name="addcostspage"),
    path('addmaincategory/<int:project_pk>/', addmaincategory, name='addmaincategory'),
    path('addsubcategory/<int:project_pk>/<int:main_category_pk>/', addsubcategory, name='addsubcategory'),
    path('addprojectcost/<int:project_pk>/<int:main_category_pk>/<int:sub_category_pk>/', addprojectcost, name='addprojectcost'),
    path('get_project_expected_costs/<int:subcategory_id>/', get_project_expected_costs, name='get_project_expected_costs'),
    path('gettotaldata/<int:project_pk>/', gettotaldata, name='gettotaldata'),
    path('fullreport/', fullreport, name='fullreport'),
    #-----------------------------------------------
    path('get_categories/', GetCategoriesView.as_view(), name='get_categories'),
    path('get_category_workers/', GetCategoryWorkers.as_view(), name='get_category_workers'),
    path('get_category_subs/', GetCategorySubs.as_view(), name='get_category_subs'),
    path('showfullreport/', showfullreport, name='showfullreport'),
    path('getselectedclientaddress/<int:pk>/', getselectedclientaddress, name='getselectedclientaddress'),
]

