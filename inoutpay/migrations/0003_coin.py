# Generated by Django 4.2.4 on 2023-12-20 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inoutpay', '0002_delete_inpay'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(blank=True, max_length=200, null=True, verbose_name=' اسم العملة')),
                ('ammount_in_egyption_pound', models.FloatField(blank=True, null=True, verbose_name='  القيمة بالجنية المصرى')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name=' تاريخ اخر تعديل')),
            ],
            options={
                'verbose_name': '  عملة',
                'verbose_name_plural': 'العملات',
            },
        ),
    ]