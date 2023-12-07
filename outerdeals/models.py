from django.db import models

from userdata.models import User

# Create your models here.
class OfficeCosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='who_did_this', null=True,blank=True,verbose_name = " القائم بالشراء") 
    ammount = models.IntegerField(verbose_name = " المصروف",null=True,blank=True)
    date_added = models.DateTimeField(verbose_name = " تاريخ الصرف",auto_now_add=True,null=True,blank=True) 
    cost_reason = models.CharField(verbose_name="سبب الصرف", max_length=200, null=True, blank=True)
    paid = models.IntegerField(verbose_name = " المدفوع",default = 0,null=True,blank=True)
    file = models.FileField(upload_to='costs_files/', null=True,blank=True,verbose_name = "   فاتورة ")

    def __str__(self) :
        return str(self.ammount)
    class Meta:
        verbose_name_plural = ' استهلاكات المكتب '
        verbose_name='  مصروف '
