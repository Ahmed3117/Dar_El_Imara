# Generated by Django 4.2.4 on 2024-01-21 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0035_remove_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='inpay',
            name='total_paid',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' مجموع المدفوع حتى الان'),
        ),
    ]
