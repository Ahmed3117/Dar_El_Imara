# Generated by Django 4.2.6 on 2023-11-06 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0008_designwork_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcosts',
            name='for_witch_worker',
            field=models.ForeignKey(blank=True, limit_choices_to={'type': 'W'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paid_worker', to='maindata.employee', verbose_name='  العامل المستلم'),
        ),
    ]