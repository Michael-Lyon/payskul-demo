# Generated by Django 4.1.3 on 2023-09-28 01:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0029_securityquestion_delete_education_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="pin",
            field=models.PositiveIntegerField(blank=True, default=123456, null=True),
        ),
    ]
