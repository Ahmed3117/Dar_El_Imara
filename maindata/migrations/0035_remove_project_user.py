# Generated by Django 4.2.4 on 2024-01-20 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0034_alter_project_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
    ]
