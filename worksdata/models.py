
from django.db import models
from maindata.models import Project, ProjectKhamatCosts, ProjectWorkersReserves
from django.core.validators import MinValueValidator
class DesignWorkType(models.Model):
    type = models.CharField(verbose_name="شغلانة ", max_length=100)
    unit_price = models.IntegerField(verbose_name=" سعر الوحدة", default=1,validators=[MinValueValidator(1)])
    mitr_price = models.IntegerField(verbose_name=" سعر المتر", default=1,validators=[MinValueValidator(1)])

    class Meta:
        verbose_name_plural = ' انواع شغل التصميم'
        verbose_name = 'شغلانة'

    def __str__(self):
        if self.type:
            return self.type
        else:
            return '---'
        
# project works
class DesignWork(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("mitr", "بالمتر"),
        ("unit", "بالوحدة"),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="المشروع")
    worktype = models.ForeignKey(DesignWorkType,on_delete=models.CASCADE,verbose_name="نوع الشغلانة",)
    account_way = models.CharField(verbose_name="نوع الحسبة", choices=accountway, max_length=10, default="mitr", blank=True,help_text ="اختيار بالمتر معناه ان سيتم احتساب سعر التصميم عن طريق ضرب الكمية فى سعر المتر الواحد للشغلانة , اختيار بالوحده يعنى سعر التصميم يساوى ضرب الكمية فى سعر الوحدة للشغلانة , اختيار مقطعية يعنى سعر التصميم يساوى الكمية مباشرة")
    ammount = models.IntegerField(verbose_name="الكمية", validators=[MinValueValidator(1)])
    date_added = models.DateTimeField(verbose_name="تاريخ الاضافة", auto_now_add=True, null=True, blank=True)
    work_cost = models.IntegerField(verbose_name=" المجموع", default=0,validators=[MinValueValidator(0)], null=True, blank=True)
    description = models.CharField(verbose_name=" وصف", max_length=1000,null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True,blank=True,verbose_name = "   ملف ")
    notes = models.CharField(verbose_name=" ملاحظات", max_length=1000, null=True, blank=True)
    
    def workcost(self,theammount):
        try:
            if self.account_way == 'direct':
                return theammount 
            if self.account_way == 'mitr':
                return theammount * self.worktype.mitr_price
            if self.account_way == 'unit':
                return theammount * self.worktype.unit_price
        except:
            return 0

    def save(self, *args, **kwargs):
        if self.pk is not None:
            olddesignwork = DesignWork.objects.get(id = self.pk)
            oldworkcost = olddesignwork.work_cost
            oldworktype = olddesignwork.worktype
            oldammount = olddesignwork.ammount
            super(DesignWork, self).save(*args, **kwargs)
            newammount = self.ammount
            difference_between_ammounts = newammount - oldammount
            self.work_cost = oldworkcost + self.workcost(difference_between_ammounts)
            super(DesignWork, self).save(*args, **kwargs)
        else:
            self.work_cost = self.workcost(self.ammount)
            super(DesignWork, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return self.worktype.type
        except:
            return '---'

    class Meta:
        verbose_name_plural = ' اعمال التصميم   '
        verbose_name='  عمل'
# الاشراف الهندسى
class EngSupervision(models.Model):
    accountway = (
        ("direct", "مقطعية"),
        ("percent", "نسبة"),
    )
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name="المشروع")
    account_way = models.CharField(verbose_name="نوع الحسبة", choices=accountway, max_length=10, default="direct", blank=True,help_text ="اختيار نسبة معناه ان سيتم احتساب سعر الاشراف عن طريق ضرب الكمية (%) فى ( مجموع حساب الخامات الفعلية + مجموع حساب مستحقات العاملين ) مقسوما على 100 , اختيار مقطعية يعنى سعر الاشراف يساوى الكمية مباشرة")
    ammount = models.IntegerField(verbose_name="الكمية", default=0, validators=[MinValueValidator(0)])
    date_added = models.DateTimeField(verbose_name="تاريخ الاضافة", auto_now_add=True, null=True, blank=True)
    all_costs = models.IntegerField(verbose_name=" جميع التكاليف", default=1, editable=False, null=True, blank=True)
    work_cost = models.IntegerField(verbose_name=" الحساب المستحق", default=1, null=True, blank=True)
    description = models.CharField(verbose_name=" وصف", max_length=1000,null=True, blank=True)

    def workcost(self):
        total_khamat_cost = 0
        total_workersreserves_cost = 0
        if self.account_way == 'percent':
            khamat_costs = ProjectKhamatCosts.objects.filter(project = self.project)
            workersreserves_costs = ProjectWorkersReserves.objects.filter(project = self.project)

            for cost in khamat_costs:
                if cost.total_cost_for_this_khama:
                    total_khamat_cost = total_khamat_cost + cost.total_cost_for_this_khama
        
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
                if cost.total_cost_for_this_khama:
                    total_khamat_cost = total_khamat_cost + cost.total_cost_for_this_khama
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
            return '---'

    class Meta:
        verbose_name_plural = ' حسبة الاشراف الهندسى '
        verbose_name='  عمل'
