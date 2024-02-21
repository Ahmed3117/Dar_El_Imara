# Generated by Django 5.0 on 2023-12-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name=' الاسم')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name=' الموبايل')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name=' العنوان')),
                ('mail', models.CharField(blank=True, max_length=200, null=True, verbose_name=' الايميل')),
            ],
            options={
                'verbose_name': '  معلومات ',
                'verbose_name_plural': '  معلومات المكتب ',
            },
        ),
    ]
