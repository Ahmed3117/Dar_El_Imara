# Generated by Django 4.2.4 on 2023-11-26 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0015_alter_expectedprojectcosts_build_subjects_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maindata.client', verbose_name='عميل'),
        ),
    ]
