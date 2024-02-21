# Generated by Django 4.2.4 on 2023-12-08 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0004_alter_employee_options_remove_employee_type_and_more'),
        ('maindata', '0008_projectkhamatcosts_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectkhamatcosts',
            name='market',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.marketsources', verbose_name='المحل'),
        ),
    ]
