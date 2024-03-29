# Generated by Django 4.2.4 on 2023-12-20 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subdata', '0002_khama'),
        ('maindata', '0010_expectedprojectcosts_file_expectedprojectcosts_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expectedprojectcosts',
            name='build_subjects',
        ),
        migrations.RemoveField(
            model_name='expectedprojectcosts',
            name='build_subjects_cost',
        ),
        migrations.AddField(
            model_name='expectedprojectcosts',
            name='khama',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subdata.khama', verbose_name='خامة'),
        ),
        migrations.AddField(
            model_name='expectedprojectcosts',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='  الكمية'),
        ),
        migrations.AddField(
            model_name='expectedprojectcosts',
            name='total_cost_for_this_khama',
            field=models.IntegerField(blank=True, null=True, verbose_name='  المجموع'),
        ),
    ]
