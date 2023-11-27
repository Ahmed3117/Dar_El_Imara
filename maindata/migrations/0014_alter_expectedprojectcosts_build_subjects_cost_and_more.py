# Generated by Django 4.2.4 on 2023-11-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0013_expectedprojectcosts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedprojectcosts',
            name='build_subjects_cost',
            field=models.IntegerField(blank=True, max_length=200, null=True, verbose_name=' تكلفة الخامات'),
        ),
        migrations.AlterField(
            model_name='expectedprojectcosts',
            name='workers_reserves_cost',
            field=models.IntegerField(blank=True, max_length=200, null=True, verbose_name=' تكلفة المصنعيات'),
        ),
    ]
