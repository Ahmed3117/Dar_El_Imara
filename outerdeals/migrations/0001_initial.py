# Generated by Django 4.2.4 on 2023-12-07 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userdata', '0004_alter_employee_options_remove_employee_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeCosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.IntegerField(blank=True, null=True, verbose_name=' المصروف')),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True, verbose_name=' تاريخ الصرف')),
                ('cost_reason', models.CharField(blank=True, max_length=200, null=True, verbose_name='سبب الصرف')),
                ('paid', models.IntegerField(blank=True, default=0, null=True, verbose_name=' المدفوع')),
                ('file', models.FileField(blank=True, null=True, upload_to='costs_files/', verbose_name='   فاتورة ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='who_did_this', to='userdata.user', verbose_name=' القائم بالشراء')),
            ],
            options={
                'verbose_name': '  مصروف ',
                'verbose_name_plural': ' استهلاكات المكتب ',
            },
        ),
    ]
