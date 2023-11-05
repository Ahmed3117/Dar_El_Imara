from django.db import models
import random
from datetime import datetime

class CategoryDetail(models.Model):
    pay_category = models.CharField(verbose_name="اسم البند ", max_length=100, blank=True , null=True)

    class Meta:
        verbose_name_plural = '   البنود فرعية'
        verbose_name = 'بند فرعى'

    def __str__(self):
        return self.pay_category
class DesignWorkType(models.Model):
    type = models.CharField(verbose_name="شغلانة ", max_length=100, blank=True , null=True)
    unit_price = models.IntegerField(verbose_name=" سعر الوحدة", default=1, null=True, blank=True)
    mitr_price = models.IntegerField(verbose_name=" سعر المتر", default=1, null=True, blank=True)

    class Meta:
        verbose_name_plural = ' انواع شغل التصميم'
        verbose_name = 'شغلانة'

    def __str__(self):
        return self.type

class EmployeeCategory(models.Model):
    categorytype = (
        ("E", "هندسى"),
        ("T", "فنى"),
    )
    category = models.CharField(verbose_name=" التصنيف", max_length=100,null=True, blank=True)
    category_type = models.CharField(verbose_name="نوع التصنيف", choices=categorytype, max_length=10, default="T", blank=True)
    class Meta:
        verbose_name_plural = '   تصنيف الموظفين '
        verbose_name = ' تصنيف'

    def __str__(self):
        return self.category
class User(models.Model):
    name = models.CharField(verbose_name="الاسم", max_length=200, null=True, blank=True)
    national_id = models.CharField(verbose_name="الرقم القومى", max_length=14, null=True, blank=True)
    phone_number = models.CharField(verbose_name="رقم التليفون", max_length=20, null=True, blank=True)
    address = models.CharField(verbose_name="العنوان", max_length=100, null=True, blank=True)
    notes = models.CharField(verbose_name="ملاحظات", max_length=200, null=True, blank=True)
    code = models.CharField(verbose_name="الكود", max_length=12, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate the code
            current_date = datetime.now()
            year = current_date.strftime("%y")
            month = current_date.strftime("%m")
            day = current_date.strftime("%d")
            random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(5))
            self.code = f"{year}{month}{day}{random_numbers}"

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Client(User):
    class Meta:
        verbose_name_plural = 'العملاء'
        verbose_name = 'عميل'

class Employee(User):
    user_type = (
        ("E", "مهندس"),
        ("W", "عامل"),
    )
    type = models.CharField(verbose_name="النوع", choices=user_type, max_length=10, default="W", blank=True)
    category = models.ForeignKey('EmployeeCategory', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="التصنيف")
    class Meta:
        verbose_name_plural = 'الموظفين'
        verbose_name = 'موظف'

# project works
class DesignWork(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("mitr", "بالمتر"),
        ("unit", "بالوحدة"),
    )
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المشروع")
    worktype = models.ForeignKey(DesignWorkType,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="نوع الشغلانة",)
    account_way = models.CharField(verbose_name="نوع الحسبة", choices=accountway, max_length=10, default="mitr", blank=True)
    ammount = models.IntegerField(verbose_name="الكمية", default=0, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="تاريخ الاضافة", auto_now_add=True, null=True, blank=True)
    work_cost = models.IntegerField(verbose_name=" المجموع", default=1, editable=False, null=True, blank=True)
    description = models.CharField(verbose_name=" وصف", max_length=1000,null=True, blank=True)

    def workcost(self):
        try:
            if self.account_way == 'direct':
                return self.ammount 
            if self.account_way == 'mitr':
                return self.ammount * self.worktype.mitr_price
            if self.account_way == 'unit':
                return self.ammount * self.worktype.unit_price
        except:
            return 0

    def save(self, *args, **kwargs):
        # super(SellProcess, self).save(*args, **kwargs)
        self.work_cost = self.workcost()
        super(DesignWork, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return self.worktype.type
        except:
            pass

    class Meta:
        verbose_name_plural = ' اعمال التصميم الخاصة بالمشاريع '
        verbose_name='  عمل'
# الاشراف الهندسى
class EngSupervision(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("percent", "نسبة"),
    )
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المشروع")
    account_way = models.CharField(verbose_name="نوع الحسبة", choices=accountway, max_length=10, default="mitr", blank=True)
    ammount = models.IntegerField(verbose_name="الكمية", default=0, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="تاريخ الاضافة", auto_now_add=True, null=True, blank=True)
    all_costs = models.IntegerField(verbose_name=" جميع التكاليف", default=1, editable=False, null=True, blank=True)
    work_cost = models.IntegerField(verbose_name=" الحساب المستحق", default=1, editable=False, null=True, blank=True)

    def workcost(self):
        work_costs = []
        total_work_cost = 0
        if self.account_way == 'percent':
            try:
                work_costs = ProjectCosts.objects.filter(project = self)
                for cost in work_costs:
                    total_work_cost = total_work_cost + cost.ammount
                return total_work_cost * self.ammount
            except:
                return 0
        elif self.account_way == 'direct':
            return self.ammount
        else:
            return 0
    def allcosts(self):
        work_costs = []
        total_work_cost = 0
        try:
            work_costs = ProjectCosts.objects.filter(project = self)
            for cost in work_costs:
                total_work_cost = total_work_cost + cost.ammount
            return total_work_cost 
        except:
            return 0

    def save(self, *args, **kwargs):
        # super(SellProcess, self).save(*args, **kwargs)
        self.work_cost = self.workcost()
        self.all_costs = self.allcosts()
        super(EngSupervision, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return self.project.project_name
        except:
            pass

    class Meta:
        verbose_name_plural = ' اعمال الاشراف الهندسى الخاصة بالمشاريع '
        verbose_name='  عمل'

class ProjectCosts(models.Model):
    Payreasoncategory = (
        ("a", "مصنعيات"),
        ("b", "خامات"),
    )
    whopaid = (
        ("o", "المكتب"),
        ("w", "عامل"),
        ("e", "مهندس"),
        ("c", "العميل"),
    )
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    who_paid = models.CharField(verbose_name="  القائم بالدفع",choices=whopaid, default='o',  max_length=10, null=True, blank=True)
    # if who_paid == 'c' :  column should appear
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " العميل") 
    # if who_paid == 'e' :  column should appear
    engineers = models.ForeignKey('Employee', on_delete=models.SET_NULL,related_name='engineers', null=True,blank=True,verbose_name = " المهندس",limit_choices_to={"type": "E"}) 
    # if who_paid == 'w' :  column should appear
    workers = models.ForeignKey('Employee', on_delete=models.SET_NULL,related_name='workers', null=True,blank=True,verbose_name = " العامل",limit_choices_to={"type": "W"}) 
    
    ammount = models.IntegerField(verbose_name = " القيمة",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    pay_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    pay_reason_category = models.CharField(verbose_name=" بند الصرف",choices=Payreasoncategory, max_length=10, null=True, blank=True)
    # if Payreasoncategory == a: pay_category_detail column should appear
    pay_category_detail = models.ForeignKey('CategoryDetail', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " بند فرعى") 
    # if Payreasoncategory == b: market column should appear
    market = models.ForeignKey('MarketSources', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " المورد") 
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    
    def save(self, *args, **kwargs):
        if self.who_paid in ['o','c', 'e', 'w']:
            # If 'who_paid' is one of the specified values, ensure the other fields are set to null
            if self.who_paid == 'o':
                self.client = None
                self.engineers = None
                self.workers = None
            elif self.who_paid == 'c':
                self.engineers = None
                self.workers = None
            elif self.who_paid == 'e':
                self.client = None
                self.workers = None
            elif self.who_paid == 'w':
                self.client = None
                self.engineers = None
        if self.pay_reason_category in ['a','b']:
            # If 'who_paid' is one of the specified values, ensure the other fields are set to null
            if self.pay_reason_category == 'a':
                self.market = None
            elif self.pay_reason_category == 'b':
                self.pay_category_detail = None

        super(ProjectCosts, self).save(*args, **kwargs)
    
    def get_name_of_paid_person(self):
        if self.who_paid == 'c' and self.client:
            return self.client.name  
        elif self.who_paid == 'e' and self.engineers:
            return self.engineers.name  
        elif self.who_paid == 'w' and self.workers:
            return self.workers.name  
        return "-"
    def get_name_of_pay_reason_category(self):
        if self.pay_reason_category == 'a' and self.pay_category_detail:
            return self.pay_category_detail.pay_category  
        elif self.pay_reason_category == 'b' and self.market:
            return self.market.sourcemarket  

        return "-"
    
    get_name_of_paid_person.short_description = " اسم القائم بالدفع" 
    get_name_of_pay_reason_category.short_description = " تفصيل البند " 
    
    def __str__(self) :
        return str(self.ammount)
    class Meta:
        verbose_name_plural = '   مصروفات المشروع'
        verbose_name='  مصروف '

class Project(models.Model):
    project_name = models.CharField(verbose_name="اسم المشروع", max_length=200)
    project_address = models.CharField(verbose_name=" عنوان المشروع", max_length=200, null=True, blank=True)
    client = models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="عميل")
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
    # Workmanship =  models.IntegerField(verbose_name = "المصنعية",default = 0 ,null=True,blank=True)
    # other_cost = models.IntegerField(verbose_name = "تكاليف اخرى",default = 0 ,null=True,blank=True)
    
    # مجموع حساب اعمال التصميم
    def projecttotaldesignworkscosts(self):
        designworks = DesignWork.objects.filter(project = self)
        totaldesignworkscosts = 0
        for work in designworks :
            totaldesignworkscosts += work.work_cost
        return totaldesignworkscosts
    # التكاليف التى تم دفعها مباشرة من خلال العميل
    def paiddirectlybyclient(self):
        paid_by_client = ProjectCosts.objects.filter(project = self , who_paid = 'c')
        total_paid_by_client = 0
        for paid in paid_by_client :
            total_paid_by_client += paid.ammount
        return total_paid_by_client
    # مجموع حساب اعمال الاشراف الهندسى
    def projectdeservedengsupervisioncosts(self):
        engsupervisionworks = EngSupervision.objects.filter(project = self)
        totalengsupervisionworkscosts = 0
        for work in engsupervisionworks :
            totalengsupervisionworkscosts += work.work_cost
        return totalengsupervisionworkscosts
    #   محموع حساب كل الاعمال
    def alldeservedmoney(self):
        deserved_money = self.projecttotaldesignworkscosts() + self.projectdeservedengsupervisioncosts()
        return deserved_money
    # مجموع تكاليف اعمال الاشراف الهندسى
    def totalprojectengsupervisioncosts(self):
        projectcosts = EngSupervision.objects.filter(project = self)
        total_project_costs = 0
        for cost in projectcosts :
            total_project_costs += cost.all_costs
        return total_project_costs

    # مجموع ما تم الحصول عليه مكن مستحقات العاملين
    # def totalprojectcosts(self):
    #     projectstuffcost = ProjectCosts.objects.filter(project = self)
    #     stuffcost = 0
    #     for pay in projectstuffcost :
    #         stuffcost += pay.ammount
    #     return stuffcost
    # مجموع الوارد المالى
    def totalinpaycosts(self):
        inpaycosts = inPay.objects.filter(project = self)
        total_inpay_costs = 0
        for inpay in inpaycosts :
            total_inpay_costs += inpay.paid
        return total_inpay_costs + self.paiddirectlybyclient()
    
    # باقىى الحساب
    def charge(self):
        charge = self.totalinpaycosts() - self.alldeservedmoney() -self.totalprojectengsupervisioncosts() + self.discount
        return int(charge)

    totalprojectengsupervisioncosts.short_description = " مصاريف المشروع " 
    projecttotaldesignworkscosts.short_description = " حساب اعمال التصميم" 
    projectdeservedengsupervisioncosts.short_description = " حساب اعمال الاشراف الهندسى" 
    alldeservedmoney.short_description = ' محموع حساب كل الاعمال '
    totalinpaycosts.short_description = " مجموع الوارد المالى" 
    charge.short_description = " باقى الحساب" 
    class Meta:
        verbose_name_plural = 'المشاريع'
        verbose_name = 'مشروع'

    def __str__(self):
        try:
            return self.project_name
        except:
            return '--'

class inPay(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    paid = models.IntegerField(verbose_name = "دفعة مالية",null=True,blank=True)
    giver = models.CharField(verbose_name="المسلم", max_length=100, blank=True,null=True)
    recipient = models.CharField(verbose_name="المستلم", max_length=100, blank=True,null=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الاضافة",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='inpay_files/', null=True,blank=True,verbose_name = "   فاتورة ")

    def __str__(self) :
        return str(self.paid)
    class Meta:
        verbose_name_plural = ' الوارد المالى'
        verbose_name='  دفعة مالية'

# السحب من الخزينة لصالح مشاريع معينة
class OutPay(models.Model):
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    user = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "القائم بالسحب") 
    ammount = models.IntegerField(verbose_name = " القيمة",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    pay_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    # pay_reason_category = models.CharField(verbose_name=" بند الصرف",choices=Payreasoncategory, max_length=10, null=True, blank=True)
    # pay_category_detail = models.ForeignKey('CategoryDetail', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "تفصيل البند") 
    # paid = models.IntegerField(verbose_name = " المدفوع",default = 0,null=True,blank=True)
    file = models.FileField(upload_to='out_pay_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    
    def __str__(self) :
        return str(self.ammount)
    class Meta:
        verbose_name_plural = ' قائمة السحب من الخزينة'
        verbose_name=' عملية سحب '

class OfficeCosts(models.Model):
    cost_type = (
        ("1", "طلبات شغل "),
        ("2", "استهلاك مكتب"),
    )
    # project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    costtype = models.CharField(verbose_name="النوع", choices=cost_type, max_length=3, default="1", blank=True)
    ammount = models.IntegerField(verbose_name = " المصروف",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    cost_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    market = models.ForeignKey('MarketSources', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "مصدر الشراء") 
    paid = models.IntegerField(verbose_name = " المدفوع",default = 0,null=True,blank=True)
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    
    def charge(self):
        charge = self.ammount  - self.paid
        return int(charge)

    charge.short_description = " باقى الحساب" 

    def __str__(self) :
        return str(self.ammount)
    class Meta:
        verbose_name_plural = ' استهلاكات المكتب '
        verbose_name='  مصروف '

class MarketSources(models.Model):
    sourcemarket = models.CharField(verbose_name="الاسم", max_length=200, null=True, blank=True)
    phone_number = models.CharField(verbose_name="رقم التليفون", max_length=20, null=True, blank=True)
    address = models.CharField(verbose_name="العنوان", max_length=100, null=True, blank=True)
    class Meta:
        verbose_name_plural = ' موردين'
        verbose_name = ' مورد'

    def __str__(self):
        return self.sourcemarket

# class CompanyMarketsWork(models.Model):
#     ProjectCosts = models.OneToOneField('ProjectCosts', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "عملية استهلاكية") 
#     ammount = models.IntegerField(verbose_name = " المصروف",null=True,blank=True)
#     date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
#     file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")
#     source = models.ForeignKey('MarketSources', on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "مصدر الشراء") 

#     def __str__(self) :
#         return str(self.ammount)
#     class Meta:
#         verbose_name_plural = ' التعامل مع الاسواق الشرائية'
#         verbose_name='  تعامل '
