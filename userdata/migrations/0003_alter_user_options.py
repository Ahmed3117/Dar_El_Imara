# Generated by Django 4.2 on 2023-12-01 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0002_alter_employee_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'مستخدم', 'verbose_name_plural': 'المستخدمين'},
        ),
    ]
