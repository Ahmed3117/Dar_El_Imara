# Generated by Django 5.0.6 on 2024-07-03 00:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksdata', '0013_alter_designwork_work_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designwork',
            name='ammount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='الكمية'),
        ),
    ]