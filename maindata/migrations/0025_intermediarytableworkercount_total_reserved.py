# Generated by Django 4.2.4 on 2023-12-24 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0024_intermediarytableworkercount'),
    ]

    operations = [
        migrations.AddField(
            model_name='intermediarytableworkercount',
            name='total_reserved',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name=' اجمالى المستحق'),
        ),
    ]
