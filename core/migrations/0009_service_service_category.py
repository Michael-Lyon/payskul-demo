# Generated by Django 4.1.3 on 2023-01-04 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_transaction_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="service_category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.service_category",
            ),
        ),
    ]
