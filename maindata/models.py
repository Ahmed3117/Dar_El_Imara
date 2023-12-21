from django.db import models
import random
from datetime import datetime
# from inoutpay.models import Coin
from subdata.models import CategoryDetail, Khama,SubCategoryDetail,EmployeeCategory
from userdata.models import User,Employee,MarketSources
# from inoutpay.models import inPay
# from worksdata.models import DesignWorkType
# from inoutpay.models import inPay

class Coin(models.Model):
    coin = models.CharField(verbose_name=" اسم العملة", max_length=200, null=True, blank=True) 
    ammount_in_egyption_pound = models.FloatField(verbose_name = "  القيمة بالجنية المصرى",null=True,blank=True)
    date_updated = models.DateTimeField(auto_now=True,verbose_name = " تاريخ اخر تعديل",null=True,blank=True)
    def __str__(self) :
        if self.coin:
            return str(self.coin)
        else:
            return '---'
    class Meta:
        verbose_name_plural = 'العملات'
        verbose_name='  عملة'


class inPay(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL,related_name='inpaypro', null=True,blank=True,verbose_name = "المشروع") 
    paid = models.IntegerField(verbose_name = "دفعة مالية",null=True,blank=True)
    giver = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المسلم", blank=True,null=True,limit_choices_to={"type": "C"})
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المستلم",related_name='recipant', blank=True,null=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='inpay_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    def __str__(self) :
        return str(self.paid)
    class Meta:
        verbose_name_plural = ' الوارد المالى'
        verbose_name='  دفعة مالية'

class ExpectedProjectCosts(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    main_category_detail = models.ForeignKey(CategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند اساسى") 
    sub_category_detail = models.ForeignKey(SubCategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند فرعى")
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    workers_reserves = models.CharField(verbose_name=" تفاصيل المصنعيات", max_length=200, null=True, blank=True)
    workers_reserves_cost = models.IntegerField(verbose_name=" تكلفة المصنعيات",  null=True, blank=True)
    # build_subjects = models.CharField(verbose_name=" تفاصيل الخامات", max_length=200, null=True, blank=True)
    # build_subjects_cost = models.IntegerField(verbose_name=" تكلفة الخامات",  null=True, blank=True)
    khama = models.ForeignKey(Khama, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "خامة")
    quantity = models.IntegerField(verbose_name="  الكمية",default = 1, null=True, blank=True)
    total_cost_for_this_khama = models.IntegerField(verbose_name="  المجموع", null=True, blank=True)
    file = models.FileField(upload_to='expectedcostsfiles/', null=True,blank=True,verbose_name = "   ملف ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.khama and self.quantity:
            khama_price = self.khama.unit_price
            self.total_cost_for_this_khama = self.quantity * khama_price
        super().save(*args, **kwargs)
    
    def __str__(self) :
        return str(self.project.project_name)

    class Meta:
        verbose_name_plural = ' المصروفات المتوقعة للمشروع'
        verbose_name='  مصروف '

class ProjectKhamatCosts(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    main_category_detail = models.ForeignKey(CategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند اساسى") 
    sub_category_detail = models.ForeignKey(SubCategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند فرعى")
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    who_paid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشترى") 
    # khama = models.CharField(verbose_name=" التوصيف", max_length=200, null=True, blank=True)
    market = models.ForeignKey(MarketSources, on_delete=models.SET_NULL,default = '', null=True,blank=True,verbose_name = "المحل") 
    # price = models.IntegerField(verbose_name=" السعر",  null=True, blank=True)
    khama = models.ForeignKey(Khama, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "خامة")
    khama_current_price = models.IntegerField(verbose_name="  سعر الخامة وقت الشراء", null=True, blank=True,editable = False)
    quantity = models.IntegerField(verbose_name="  الكمية",default = 1, null=True, blank=True)
    total_cost_for_this_khama = models.IntegerField(verbose_name="  المجموع", null=True, blank=True)
    paid = models.IntegerField(verbose_name="  المدفوع",  null=True, blank=True)
    file = models.FileField(upload_to='khamat_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.who_paid and self.paid:
            if self.who_paid.type == "C" :
                inPay.objects.create(project = self.project , paid = self.paid , giver = self.who_paid)
        if self.khama and self.quantity:
            if not self.khama_current_price:
                self.khama_current_price = self.khama.unit_price
            khama_price = self.khama_current_price
            self.total_cost_for_this_khama = self.quantity * khama_price
        super().save(*args, **kwargs)
    
    def charge(self):
        return self.total_cost_for_this_khama - self.paid
    def __str__(self) :
        return str(self.project.project_name)
    charge.short_description = "   الباقى" 
    class Meta:
        verbose_name_plural = ' خامات المشروع'
        verbose_name='  خامة '

class ProjectWorkersReserves(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    main_category_detail = models.ForeignKey(CategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند اساسى") 
    sub_category_detail = models.ForeignKey(SubCategoryDetail, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند فرعى")
    worker = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='who_did', null=True,blank=True,verbose_name = " العامل",limit_choices_to={"type": "W"}) 
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    work = models.CharField(verbose_name=" العمل", max_length=200, null=True, blank=True)
    price = models.IntegerField(verbose_name="  التكلفة المستحقة",  null=True, blank=True)
    paid = models.IntegerField(verbose_name="  المدفوع",  null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True,blank=True,verbose_name = "   ملف ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    def charge(self):
        return self.price - self.paid
    def __str__(self) :
        return str(self.project.project_name)
    charge.short_description = "   الباقى" 

    class Meta:
        verbose_name_plural = '  مستحقات العاملين'
        verbose_name='  عمل '

class Project(models.Model):
    project_name = models.CharField(verbose_name="اسم المشروع", max_length=200)
    project_address = models.CharField(verbose_name=" عنوان المشروع", max_length=200, null=True, blank=True)
    client = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="عميل",limit_choices_to={"type": "C"})
    coin = models.ForeignKey(Coin,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="عملة التعامل")
    
    # engineers = models.ManyToManyField(
    #     User,
    #     related_name='projects_as_engineer',
    #     blank=True,
    #     verbose_name="مهندس",
    #     limit_choices_to={"type": "E"}
    # )
    # workers = models.ManyToManyField(
    #     User,
    #     related_name='projects_as_worker',
    #     blank=True,
    #     verbose_name="عامل",
    #     limit_choices_to={"type": "W"}
    # )
    discount = models.IntegerField(verbose_name = "الخصم",default = 0 ,null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الانشاء",auto_now_add=True,null=True,blank=True) 
    is_done = models.BooleanField(verbose_name = "  المشروع منتهى",default=False)
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'المشاريع'
        verbose_name = 'مشروع'

    def __str__(self):
        try:
            return self.project_name
        except:
            return '-'


