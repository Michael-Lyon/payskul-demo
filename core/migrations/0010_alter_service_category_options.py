# Generated by Django 4.1.3 on 2023-03-27 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_service_service_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="service_category",
            options={
                "ordering": ("name",),
                "verbose_name": "Service Category",
                "verbose_name_plural": "Service Categories",
            },
        ),
    ]
