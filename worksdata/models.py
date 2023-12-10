
from django.db import models
from maindata.models import Project, ProjectKhamatCosts, ProjectWorkersReserves
class DesignWorkType(models.Model):
    type = models.CharField(verbose_name="شغلانة ", max_length=100, blank=True , null=True)
    unit_price = models.IntegerField(verbose_name=" سعر الوحدة", default=1, null=True, blank=True)
    mitr_price = models.IntegerField(verbose_name=" سعر المتر", default=1, null=True, blank=True)

    class Meta:
        verbose_name_plural = ' انواع شغل التصميم'
        verbose_name = 'شغلانة'

    def __str__(self):
        return self.type

# project works
class DesignWork(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("mitr", "بالمتر"),
        ("unit", "بالوحدة"),
    )
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المشروع")
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
            return '-'

    class Meta:
        verbose_name_plural = ' اعمال التصميم   '
        verbose_name='  عمل'
# الاشراف الهندسى
class EngSupervision(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("percent", "نسبة"),
    )
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المشروع")
    account_way = models.CharField(verbose_name="نوع الحسبة", choices=accountway, max_length=10, default="direct", blank=True)
    ammount = models.IntegerField(verbose_name="الكمية", null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="تاريخ الاضافة", auto_now_add=True, null=True, blank=True)
    all_costs = models.IntegerField(verbose_name=" جميع التكاليف", default=1, editable=False, null=True, blank=True)
    work_cost = models.IntegerField(verbose_name=" الحساب المستحق", default=1, editable=False, null=True, blank=True)
    description = models.CharField(verbose_name=" وصف", max_length=1000,null=True, blank=True)

    def workcost(self):
        total_khamat_cost = 0
        total_workersreserves_cost = 0
        if self.account_way == 'percent':
            khamat_costs = ProjectKhamatCosts.objects.filter(project = self.project)
            workersreserves_costs = ProjectWorkersReserves.objects.filter(project = self.project)

            for cost in khamat_costs:
                if cost.price:
                    total_khamat_cost = total_khamat_cost + cost.price
        
            for cost in workersreserves_costs:
                if cost.price:
                    total_workersreserves_cost = total_workersreserves_cost + cost.price 

            return (total_khamat_cost + total_workersreserves_cost) * self.ammount /100
        elif self.account_way == 'direct':
            return self.ammount
        else:
            return 0
    # مجموع حساب التكاليف نفسها (خامات + مصنعيات)
    def allcosts(self):
        total_khamat_cost = 0
        total_workersreserves_cost = 0
        khamat_costs = []
        workersreserves_costs =[]
        try:
            khamat_costs = ProjectKhamatCosts.objects.filter(project = self.project)
            workersreserves_costs = ProjectWorkersReserves.objects.filter(project = self.project)
            for cost in khamat_costs:
                if cost.price:
                    total_khamat_cost = total_khamat_cost + cost.price
            for cost in workersreserves_costs:
                if cost.price:
                    total_workersreserves_cost = total_workersreserves_cost + cost.price 
        except:
            pass
        return total_khamat_cost + total_workersreserves_cost
    
    def save(self, *args, **kwargs):
        # super(SellProcess, self).save(*args, **kwargs)
        self.work_cost = self.workcost()
        self.all_costs = self.allcosts()
        super(EngSupervision, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return self.project.project_name
        except:
            return '-'

    class Meta:
        verbose_name_plural = ' اعمال الاشراف الهندسى '
        verbose_name='  عمل'
