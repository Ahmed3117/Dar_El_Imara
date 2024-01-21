from django.contrib import admin
from .models import User,Employee,MarketSources
from .forms import EmployeeForm
# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ('user', 'category')
    list_filter = ('category',)
    search_fields = ( 'category',)
    # def projectinfo(self, obj):
    #     project_id = obj.id
    # printinvoice.short_description = ' تقرير '
    class Media:
        js = ('/static/admin/js/employee_types.js',)

class EmployeeInlineAdmin(admin.TabularInline):
    model = Employee
    extra = 1
    show_change_link = True
    # classes = ('collapse',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','type', 'phone_number', 'address', 'code')
    search_fields = ('type', 'name','type', 'phone_number', 'address', 'code')
    list_filter = ('type',)
    inlines = [EmployeeInlineAdmin,]
    class Media:
        js = ('/static/admin/js/employee_types.js',)

class MarketSourcesAdmin(admin.ModelAdmin):
    list_display = ('sourcemarket', 'phone_number', 'address')
    search_fields = ('sourcemarket', 'phone_number', 'address')

admin.site.register(MarketSources, MarketSourcesAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Employee, EmployeeAdmin)
