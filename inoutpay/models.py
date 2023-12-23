from django.db import models
from maindata.models import Project
from userdata.models import Employee,User
# Create your models here.

# السحب من الخزينة لصالح مشاريع معينة
class MoneyWithDraw(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "القائم بالسحب") 
    ammount = models.IntegerField(verbose_name = " القيمة",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    pay_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    # pay_reason_category = models.CharField(verbose_name=" بند الصرف",choices=Payreasoncategory, max_length=10, null=True, blank=True)
    # main_category_detail = models.ForeignKey('CategoryDetail', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "تفصيل البند") 
    # paid = models.IntegerField(verbose_name = " المدفوع",default = 0,null=True,blank=True)
    file = models.FileField(upload_to='out_pay_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    
    def __str__(self) :
        if self.ammount :
            return str(self.ammount)
        else:
            return '---'
    class Meta:
        verbose_name_plural = '  السحب من الخزينة'
        verbose_name=' عملية سحب '


