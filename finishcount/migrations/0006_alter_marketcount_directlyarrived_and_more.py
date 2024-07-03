# Generated by Django 5.0.6 on 2024-07-03 00:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finishcount', '0005_delete_intermediarytableworkercount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketcount',
            name='directlyarrived',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المدفوع'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workercount',
            name='directlyarrived',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' المدفوع'),
        ),
    ]