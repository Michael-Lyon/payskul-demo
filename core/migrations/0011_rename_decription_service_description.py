# Generated by Django 4.1.3 on 2023-03-28 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_service_category_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="service",
            old_name="decription",
            new_name="description",
        ),
    ]
