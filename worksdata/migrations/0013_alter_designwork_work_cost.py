# Generated by Django 5.0.6 on 2024-07-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksdata', '0012_alter_designwork_work_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designwork',
            name='work_cost',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' المجموع'),
        ),
    ]