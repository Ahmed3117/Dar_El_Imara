# Generated by Django 4.2.4 on 2023-12-29 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0004_alter_employee_options_remove_employee_type_and_more'),
        ('maindata', '0027_alter_intermediarytableworkercount_directlyarrived'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntermediaryTableMarketCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directlyarrived', models.IntegerField(blank=True, null=True, verbose_name=' المدفوع')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name=' تاريخ الصرف')),
                ('file', models.FileField(blank=True, null=True, upload_to='MarketCount_files/', verbose_name='   فاتورة ')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maindata.project', verbose_name='المشروع')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.marketsources', verbose_name=' المورد')),
            ],
            options={
                'verbose_name': '  تعامل ',
                'verbose_name_plural': ' تخليص حسابات العمال',
            },
        ),
    ]
