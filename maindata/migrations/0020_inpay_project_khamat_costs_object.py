# Generated by Django 4.2.4 on 2023-12-22 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0019_alter_expectedprojectcosts_total_cost_for_this_khama'),
    ]

    operations = [
        migrations.AddField(
            model_name='inpay',
            name='project_khamat_costs_object',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='maindata.projectkhamatcosts'),
        ),
    ]
