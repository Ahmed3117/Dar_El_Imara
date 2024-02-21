from django.db import models

from userdata.models import User

# Create your models here.
class OfficeCosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='who_did_this', null=True,blank=True,verbose_name = " القائم بالشراء") 
    ammount = models.IntegerField(verbose_name = " المصروف",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    cost_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")

    def __str__(self) :
        if self.ammount :
            return str(self.ammount)
        else:
            return '---'
    class Meta:
        verbose_name_plural = ' استهلاكات المكتب '
        verbose_name='  مصروف '
        
class OutDeals(models.Model):
    creditor = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='creditor_user', null=True,blank=True,verbose_name = "  الدائن") 
    debtor = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='debtor_user', null=True,blank=True,verbose_name = "  المدين") 
    ammount = models.IntegerField(verbose_name = " المبلغ",default = 0,null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " التاريخ ",auto_now_add=True,null=True,blank=True) 
    reason = models.CharField(verbose_name="سبب الدين", max_length=200, null=True, blank=True)
    paid = models.IntegerField(verbose_name = "  المدفوع حتى الان",default = 0,null=True,blank=True)
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    def charge(self):
        if self.ammount and self.paid:
            return self.ammount - self.paid 
        else :
            return 0
    charge.short_description = "   الباقى" 
    def __str__(self) :
        if self.creditor :
            return str(self.creditor)
        else:
            return '---'
    class Meta:
        verbose_name_plural = '  سلف وتعاملات اخرى '
        verbose_name='  تعامل  '
        
class MonthPay(models.Model):
    outdeal = models.ForeignKey(OutDeals, on_delete=models.SET_NULL, null=True,blank=True,verbose_name = "  العملية") 
    ammount = models.IntegerField(verbose_name = " المبلغ",default = 0,null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " التاريخ ",auto_now_add=True,null=True,blank=True) 
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")
    def save(self, *args, **kwargs):
        if self.ammount and self.outdeal:
            self.outdeal.paid += self.ammount 
            self.outdeal.save()
        super().save(*args, **kwargs)
    def __str__(self) :
        if self.creditor :
            return str(self.outdeal.creditor.name)
        else:
            return '---'

    class Meta:
        verbose_name_plural = '  اقساط '
        verbose_name='  قسط  '
