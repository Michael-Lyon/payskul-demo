# Generated by Django 4.1.3 on 2022-12-28 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_loan_options_alter_service_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="deposit_rate",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
