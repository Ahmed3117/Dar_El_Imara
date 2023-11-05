# Generated by Django 4.2.4 on 2023-11-02 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcosts',
            name='engineers',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'E'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='engineers', to='maindata.employee', verbose_name=' المهندسين'),
        ),
        migrations.AddField(
            model_name='projectcosts',
            name='workers',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'W'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='maindata.employee', verbose_name=' العمال'),
        ),
    ]
