from django.contrib import admin
from .models import CategoryDetail,SubCategoryDetail,EmployeeCategory
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


class EmployeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'category_type')
    list_filter = ('category_type',)
    search_fields = ('category',)




admin.site.register(CategoryDetail, CategoryDetailAdmin)
# admin.site.register(SubCategoryDetail, SubCategoryDetailAdmin)

# admin.site.register(EmployeeCategory, EmployeeCategoryAdmin)
