from django.db import models

# Create your models here.
class CategoryDetail(models.Model):
    main_category = models.CharField(verbose_name="اسم البند ", max_length=100, blank=True , null=True)
    class Meta:
        verbose_name_plural = '   البنود'
        verbose_name = 'بند اساسى'

    def __str__(self):
        if self.main_category:
            return self.main_category
        else: 
            return '---'

class SubCategoryDetail(models.Model):
    sub_category = models.CharField(verbose_name="اسم البند ", max_length=100, blank=True , null=True)
    main_category = models.ForeignKey(CategoryDetail, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="البند الاساسى")

    class Meta:
        verbose_name_plural = '   البنود الفرعية'
        verbose_name = 'بند فرعى'

    def __str__(self):
        if self.sub_category:
            return self.sub_category
        else:
            return ''

class EmployeeCategory(models.Model):
    categorytype = (
        ("G", "عام"),
        ("E", "هندسى"),
        ("T", "فنى"),
    )
    category = models.CharField(verbose_name=" التصنيف", max_length=100,null=True, blank=True)
    category_type = models.CharField(verbose_name="نوع التصنيف", choices=categorytype, max_length=10, default="T", blank=True)
    class Meta:
        verbose_name_plural = '   تصنيف الموظفين '
        verbose_name = ' تصنيف'

    def __str__(self):
        if self.category:
            return self.category
        else:
            return '---'


class Khama(models.Model):
    name = models.CharField(verbose_name="اسم الخامة ", max_length=100, blank=True , null=True)
    main_category = models.ForeignKey(CategoryDetail, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="البند الاساسى")
    unit_price = models.IntegerField(null=True, blank=True, verbose_name="سعر الوحده ")
    class Meta:
        verbose_name_plural = ' الخامات'
        verbose_name = ' خامة'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '---'

