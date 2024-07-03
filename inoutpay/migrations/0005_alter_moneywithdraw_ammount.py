# Generated by Django 5.0.6 on 2024-07-03 00:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inoutpay', '0004_delete_coin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneywithdraw',
            name='ammount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name=' القيمة'),
        ),
    ]
