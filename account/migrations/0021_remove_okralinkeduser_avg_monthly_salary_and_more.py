# Generated by Django 4.1.3 on 2023-07-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_rename_monthly_salary_okralinkeduser_avg_monthly_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='okralinkeduser',
            name='avg_monthly_salary',
        ),
        migrations.AddField(
            model_name='okralinkeduser',
            name='balance_ids',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='okralinkeduser',
            name='income_banks',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
