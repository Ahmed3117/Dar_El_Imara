# Generated by Django 4.2 on 2023-12-01 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0004_alter_employee_options_remove_employee_type_and_more'),
        ('maindata', '0004_alter_project_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inpay',
            name='giver',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'C'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userdata.user', verbose_name='المسلم'),
        ),
        migrations.DeleteModel(
            name='ProjectCosts',
        ),
    ]
