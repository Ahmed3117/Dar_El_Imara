# Generated by Django 5.0.6 on 2024-07-03 00:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outerdeals', '0005_alter_monthpay_ammount_alter_monthpay_outdeal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthpay',
            name='ammount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المبلغ'),
        ),
        migrations.AlterField(
            model_name='officecosts',
            name='ammount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المصروف'),
        ),
        migrations.AlterField(
            model_name='outdeals',
            name='ammount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المبلغ'),
        ),
        migrations.AlterField(
            model_name='outdeals',
            name='paid',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='  المدفوع حتى الان'),
        ),
    ]