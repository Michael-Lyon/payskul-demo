# Generated by Django 4.1.3 on 2023-09-22 07:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0027_myuserauth_delete_userauthcodes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="pin",
            field=models.CharField(
                blank=True, default="123456", max_length=15, null=True
            ),
        ),
    ]