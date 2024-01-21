from django.contrib import admin
from .models import CompanyInfo

class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name','phone','mail','address')
    search_fields = ('name','phone','mail','address')

    def has_add_permission(self, request):
        # if there's already an instance, do not allow adding
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

admin.site.register(CompanyInfo, CompanyInfoAdmin)
