# Generated by Django 4.2.4 on 2023-12-23 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finishcount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workercount',
            name='charge_reserved',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' اجمالى باقى المستحق'),
        ),
        migrations.AlterField(
            model_name='workercount',
            name='directlyarrived',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' المدفوع'),
        ),
    ]
