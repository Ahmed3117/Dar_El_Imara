# Generated by Django 5.0.6 on 2024-07-03 00:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0042_alter_projectkhamatcosts_khama_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedprojectcosts',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='  الكمية'),
        ),
        migrations.AlterField(
            model_name='expectedprojectcosts',
            name='workers_reserves_cost',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' تكلفة المصنعيات'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inpay',
            name='paid',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='دفعة مالية'),
        ),
        migrations.AlterField(
            model_name='intermediarytablemarketcount',
            name='charge_reserved',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' اجمالى باقى المستحق'),
        ),
        migrations.AlterField(
            model_name='intermediarytablemarketcount',
            name='directlyarrived',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المدفوع'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='intermediarytablemarketcount',
            name='total_paid_until_now',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' اجمالى المدفوع الى الان'),
        ),
        migrations.AlterField(
            model_name='intermediarytablemarketcount',
            name='total_reserved',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' اجمالى المستحق'),
        ),
        migrations.AlterField(
            model_name='project',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='الخصم'),
        ),
        migrations.AlterField(
            model_name='projectkhamatcosts',
            name='total_cost_for_this_khama',
            field=models.IntegerField(default=0, help_text='عبارة عن حاصل ضرب الكمية فى سعر الوحده للخامة (لاحظ : تتم المحاسبة على سعر الوحده الحالى للمنتج لكن اذا تم تغير سعر المنتج لاحقا لن ينطبق هذا التغيير على الصفوف المسجلة مسبقا ولكن ينطبق على اى صف جديد يتم اضافته, لذلك اذا تم شراء خامة بسعر معين وتم اضافتها ثم تم شراء نفس الخامة فى وقت لاحق وكان سعر الخامة قد تغير يجب اضافة عملية الشراء الجديدة كصف مستقل بدلا من تعديل الكمية فى الصف القديم لان اذا عدلت الكمية فسيحسب المجموع بناء على السعر القديم )', validators=[django.core.validators.MinValueValidator(0)], verbose_name='  المجموع'),
        ),
        migrations.AlterField(
            model_name='projectworkersreserves',
            name='paid',
            field=models.IntegerField(default=0, help_text='المبلغ الواصل للعميل', validators=[django.core.validators.MinValueValidator(0)], verbose_name='  المدفوع'),
        ),
        migrations.AlterField(
            model_name='projectworkersreserves',
            name='price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='  التكلفة المستحقة'),
        ),
    ]
