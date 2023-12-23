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
    # next field only exists to relate the ProjectKhamatCosts objects that the giver is the client so that we can update the inpay objects created on saving ProjectKhamatCosts 
    project_khamat_costs_object = models.ForeignKey('ProjectKhamatCosts', on_delete=models.CASCADE, blank=True,null=True,editable = False)
    giver = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المسلم", blank=True,null=True,limit_choices_to={"type": "C"})
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL,verbose_name="المستلم",related_name='recipant', blank=True,null=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='inpay_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    def __str__(self) :
        if self.paid:
            return str(self.paid)
        else:
            return '---'
    
    
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
    total_cost_for_this_khama = models.IntegerField(verbose_name="  المجموع", help_text = 'حاصل ضرب سعر الوحدة للمنتج فى الكمية (  اخر سعر تم اضافته او تعديله للمنتج )',null=True, blank=True)
    file = models.FileField(upload_to='expectedcostsfiles/', null=True,blank=True,verbose_name = "   ملف ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.khama and self.quantity:
            khama_price = self.khama.unit_price
            self.total_cost_for_this_khama = self.quantity * khama_price
        super().save(*args, **kwargs)
    
    def __str__(self) :
        if self.project:
            return str(self.project.project_name)
        else:
            return '---'
        

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
    khama_current_price = models.IntegerField(default = 0,verbose_name="  سعر الخامة وقت الشراء", null=True, blank=True,editable = False)
    quantity = models.IntegerField(default = 0,verbose_name="  الكمية", null=True, blank=True)
    total_cost_for_this_khama = models.IntegerField(default = 0,verbose_name="  المجموع", null=True, blank=True,help_text = "عبارة عن حاصل ضرب الكمية فى سعر الوحده للخامة (لاحظ : تتم المحاسبة على سعر الوحده الحالى للمنتج لكن اذا تم تغير سعر المنتج لاحقا لن ينطبق هذا التغيير على الصفوف المسجلة مسبقا ولكن ينطبق على اى صف جديد يتم اضافته, لذلك اذا تم شراء خامة بسعر معين وتم اضافتها ثم تم شراء نفس الخامة فى وقت لاحق وكان سعر الخامة قد تغير يجب اضافة عملية الشراء الجديدة كصف مستقل بدلا من تعديل الكمية فى الصف القديم لان اذا عدلت الكمية فسيحسب المجموع بناء على السعر القديم )")
    paid = models.IntegerField(default = 0,verbose_name="  المدفوع",  null=True, blank=True)
    file = models.FileField(upload_to='khamat_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.khama and self.quantity:
            if not self.khama_current_price:
                self.khama_current_price = self.khama.unit_price
            khama_price = self.khama_current_price
            self.total_cost_for_this_khama = self.quantity * khama_price
        super().save(*args, **kwargs)  # Save the current object first
        if self.who_paid and self.paid:
            if self.who_paid.type == "C" :
                try:
                    inpay_obj = inPay.objects.get(project_khamat_costs_object=self)
                    inpay_obj.project = self.project
                    inpay_obj.giver = self.who_paid
                    inpay_obj.paid = self.paid
                    inpay_obj.save()
                except:
                    inPay.objects.create(project=self.project, giver=self.who_paid, project_khamat_costs_object=self, paid=self.paid)
        

    
    def charge(self):
        return self.total_cost_for_this_khama - self.paid
    def __str__(self) :
        if self.project:
            return str(self.project.project_name)
        else:
            return '---'
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
        if self.project:
            return str(self.project.project_name)
        else:
            return '---'
    charge.short_description = "   الباقى" 

    class Meta:
        verbose_name_plural = '  مستحقات العاملين'
        verbose_name='  عمل '

class Project(models.Model):
    project_name = models.CharField(verbose_name="اسم المشروع",default = "---", max_length=200)
    project_address = models.CharField(verbose_name=" عنوان المشروع", max_length=200, null=True, blank=True)
    client = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="عميل",limit_choices_to={"type": "C"})
    coin = models.ForeignKey(Coin,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="عملة التعامل",help_text = "تعنى ان جميع الحسابات والارقام الحسابية المسجلة فى هذا المشروع هى بهذه العمله")
    
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
    is_done = models.BooleanField(verbose_name = "  المشروع منتهى",default=False ,help_text = "اختيار هذا المربع (تظليلة بالازرق) يعنى ان هذا المشروع تم الانتهاء منه")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'المشاريع'
        verbose_name = 'مشروع'

    def __str__(self):
        if self.project_name:
            return str(self.project_name)
        else:
            return '---'


