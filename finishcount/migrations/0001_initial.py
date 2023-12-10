# Generated by Django 4.2.4 on 2023-12-06 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userdata', '0004_alter_employee_options_remove_employee_type_and_more'),
        ('maindata', '0006_remove_projectworkersreserves_reserved_price_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directlyarrived', models.IntegerField(blank=True, null=True, verbose_name=' المدفوع')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name=' تاريخ الصرف')),
                ('file', models.FileField(blank=True, null=True, upload_to='WorkerCount_files/', verbose_name='   فاتورة ')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maindata.project', verbose_name='المشروع')),
                ('worker', models.ForeignKey(blank=True, limit_choices_to={'type': 'W'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.user', verbose_name='العامل')),
            ],
            options={
                'verbose_name': '  تعامل ',
                'verbose_name_plural': ' تخليص حسابات العمال',
            },
        ),
        migrations.CreateModel(
            name='MarketCount',
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
                'verbose_name_plural': ' تخليص حسابات الموردين',
            },
        ),
    ]