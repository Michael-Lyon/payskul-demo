# Generated by Django 4.1.3 on 2023-08-30 09:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0024_remove_okralinkeduser_registered_bank_id"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="userauthcodes",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="userauthcodes",
            name="code",
        ),
        migrations.RemoveField(
            model_name="userauthcodes",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="userauthcodes",
            name="expires_at",
        ),
    ]
