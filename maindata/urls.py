from django.contrib import admin
from django.urls import include, path
from .views import GetCategoriesView, invoice
app_name = 'maindata'

urlpatterns = [
    path('get_categories/', GetCategoriesView.as_view(), name='get_categories'),
    path('invoice/<int:pk>/', invoice, name="invoice"),
]

