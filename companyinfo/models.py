from django.db import models

# Create your models here.


# Create your models here.
class CompanyInfo(models.Model):
    name = models.CharField(verbose_name=" الاسم", max_length=200, null=True, blank=True)
    phone = models.CharField(verbose_name=" الموبايل", max_length=11, null=True, blank=True)
    address = models.CharField(verbose_name=" العنوان", max_length=200, null=True, blank=True)
    mail = models.CharField(verbose_name=" الايميل", max_length=200, null=True, blank=True)

    def __str__(self) :
        if self.name :
            return str(self.name)
        else:
            return '---'
    class Meta:
        verbose_name_plural = '  معلومات المكتب '
        verbose_name='  معلومات '