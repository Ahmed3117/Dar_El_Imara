from django.db import models
import random
from datetime import datetime
from subdata.models import CategoryDetail,SubCategoryDetail,EmployeeCategory
from userdata.models import User,Employee,MarketSources
# from inoutpay.models import inPay
# from worksdata.models import DesignWorkType
# from inoutpay.models import inPay

class inPay(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL,related_name='inpaypro', null=True,blank=True,verbose_name = "المشروع") 
    paid = models.IntegerField(verbose_name = "دفعة مالية",null=True,blank=True)
    giver = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المسلم", blank=True,null=True,limit_choices_to={"type": "C"})
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المستلم",related_name='recipant', blank=True,null=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='inpay_files/', null=True,blank=True,verbose_name = "   فاتورة ")

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
    build_subjects = models.CharField(verbose_name=" تفاصيل الخامات", max_length=200, null=True, blank=True)
    build_subjects_cost = models.IntegerField(verbose_name=" تكلفة الخامات",  null=True, blank=True)

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
    khama = models.CharField(verbose_name=" الشراء", max_length=200, null=True, blank=True)
    market = models.ForeignKey(MarketSources, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المحل") 
    price = models.IntegerField(verbose_name=" السعر",  null=True, blank=True)
    paid = models.IntegerField(verbose_name="  المدفوع",  null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.who_paid and self.paid:
            inPay.objects.create(project = self.project , paid = self.paid , 
            giver = self.who_paid)
        super().save(*args, **kwargs)
    def charge(self):
        return self.price - self.paid
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

    class Meta:
        verbose_name_plural = 'المشاريع'
        verbose_name = 'مشروع'

    def __str__(self):
        try:
            return self.project_name
        except:
            return '-'

