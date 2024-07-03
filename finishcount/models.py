from django.db import models
from maindata.models import ProjectKhamatCosts, ProjectWorkersReserves
from django.core.validators import MinValueValidator
from userdata.models import MarketSources, User
from maindata.models import Project
# Create your models here.

class WorkerCount(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    worker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "العامل" ,limit_choices_to={"type": "W"}) 
    directlyarrived = models.IntegerField(verbose_name = " المدفوع",default = 0,validators=[MinValueValidator(0)])
    # charge_reserved = models.IntegerField(verbose_name = " اجمالى باقى المستحق",null=True,blank=True,default = 0)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='WorkerCount_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    def deservedforthisproject(self):
        total_worker_cost = 0
        worker_costs = ProjectWorkersReserves.objects.filter(project = self.project,worker = self.worker)
        for cost in worker_costs:
            if cost.price:
                total_worker_cost = total_worker_cost + cost.price 
        return total_worker_cost
    
    def alreadypaidforthisproject(self):
        total_worker_paid = 0
        total_directly_paid = 0
        worker_costs = ProjectWorkersReserves.objects.filter(project = self.project,worker = self.worker)
        for cost in worker_costs:
            if cost.paid:
                total_worker_paid = total_worker_paid + cost.paid 
        
        directly_paid_costs = WorkerCount.objects.filter(project = self.project,worker = self.worker)
        for cost in directly_paid_costs:
            if cost.directlyarrived:
                total_directly_paid = total_directly_paid + cost.directlyarrived 
                
        return total_worker_paid + total_directly_paid
    
    def charge(self):
        return (self.deservedforthisproject() - self.alreadypaidforthisproject())

    deservedforthisproject.short_description = ' المستحق لهذا المشروع '
    alreadypaidforthisproject.short_description = ' المدفوع بالفعل لهذا المشروع '
    charge.short_description = ' الباقى '
    def __str__(self) :
        if self.project:
            return str(self.project.project_name)
        else:
            return '---'
    class Meta:
        verbose_name_plural = ' تخليص حسابات العمال'
        verbose_name='  تعامل '
# جدول وسيط بين تلخيص حسابات العاملين وبين مستحقات العملين

class MarketCount(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "المشروع") 
    source = models.ForeignKey(MarketSources, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = " المورد") 
    directlyarrived = models.IntegerField(verbose_name = " المدفوع",validators=[MinValueValidator(0)]) 
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='MarketCount_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    
    def deservedforthisproject(self):
        total_khamat_cost = 0
        khamat_costs = ProjectKhamatCosts.objects.filter(project = self.project,market=self.source)
        for cost in khamat_costs:
            if cost.total_cost_for_this_khama:
                total_khamat_cost = total_khamat_cost + cost.total_cost_for_this_khama 
        return total_khamat_cost
    
    def alreadypaidforthisproject(self):
        total_khamat_paid = 0
        total_directly_paid = 0
        khamat_costs = ProjectKhamatCosts.objects.filter(project = self.project,market=self.source)
        for cost in khamat_costs:
            if cost.paid :
                total_khamat_paid = total_khamat_paid + cost.paid 
                
        directly_paid_costs = MarketCount.objects.filter(project = self.project,source=self.source)
        for cost in directly_paid_costs:
            if cost.directlyarrived:
                total_directly_paid = total_directly_paid + cost.directlyarrived 
        return total_khamat_paid + total_directly_paid
    def charge(self):
        return (self.deservedforthisproject() - self.alreadypaidforthisproject())
    deservedforthisproject.short_description = ' المستحق لهذا المورد لهذا المشروع '
    alreadypaidforthisproject.short_description = ' المدفوع بالفعل   '
    charge.short_description = ' الباقى '
    def __str__(self) :
        if self.project:
            return str(self.project.project_name)
        else:
            return '---'
    class Meta:
        verbose_name_plural = ' تخليص حسابات الموردين'
        verbose_name='  تعامل '