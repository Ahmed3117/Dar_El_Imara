from django.db import models
from maindata.models import EmployeeCategory
from datetime import datetime
import random
from django.core.exceptions import ValidationError


def validate_name_length(value):
    """
    Custom validator to ensure the name field has at least 3 words.
    """
    words = value.split()
    if len(words) < 3:
        raise ValidationError("الاسم لابد ان يكون ثلاثى او اكثر")

class User(models.Model):
    user_type = (
        ("C", "عميل"),
        ("E", "مهندس"),
        ("W", "عامل"),
    )
    type = models.CharField(verbose_name="النوع", choices=user_type, max_length=10, default="C", null=True, blank=True)
    name = models.CharField(verbose_name="الاسم", max_length=200, validators=[validate_name_length])
    # national_id = models.CharField(verbose_name="الرقم القومى", max_length=14, null=True, blank=True)
    phone_number = models.CharField(verbose_name="رقم التليفون", max_length=20, null=True, blank=True)
    address = models.CharField(verbose_name="العنوان", max_length=100, null=True, blank=True)
    notes = models.CharField(verbose_name="ملاحظات", max_length=200, null=True, blank=True)
    code = models.CharField(verbose_name="الكود", max_length=12, editable=False, null=True, blank=True)
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return '---'
        
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate the code
            current_date = datetime.now()
            year = current_date.strftime("%y")
            month = current_date.strftime("%m")
            day = current_date.strftime("%d")
            random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(4))
            if self.type == 'E' :
                self.code = f"E{year}{month}{day}{random_numbers}"
            elif self.type == 'C' :
                self.code = f"C{year}{month}{day}{random_numbers}"
            else:
                self.code = f"W{year}{month}{day}{random_numbers}"

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'المستخدمين'
        verbose_name = 'مستخدم'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="المستخدم")
    category = models.ForeignKey(EmployeeCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="التصنيف")

    class Meta:
        verbose_name_plural = 'بيانات اضافية للموظفين'
        verbose_name = 'بيانات اضافية للموظف'

class MarketSources(models.Model):
    sourcemarket = models.CharField(verbose_name="الاسم", max_length=200)
    phone_number = models.CharField(verbose_name="رقم التليفون", max_length=20, null=True, blank=True)
    address = models.CharField(verbose_name="العنوان", max_length=100, null=True, blank=True)
    class Meta:
        verbose_name_plural = ' موردين'
        verbose_name = ' مورد'

    def __str__(self):
        if self.sourcemarket:
            return self.sourcemarket
        else:
            return '---'
        
