from django.contrib import admin
from .models import CompanyInfo
# Register your models here.


class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name','phone','mail','address')
    search_fields = ('name','phone','mail','address')
  

admin.site.register(CompanyInfo,CompanyInfoAdmin)