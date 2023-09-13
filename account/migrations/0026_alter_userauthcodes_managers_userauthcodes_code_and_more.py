# Generated by Django 4.1.3 on 2023-08-30 09:22

from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0025_alter_userauthcodes_managers_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="userauthcodes",
            managers=[
                ("expired", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name="userauthcodes",
            name="code",
            field=models.CharField(default="123456", max_length=10),
        ),
        migrations.AddField(
            model_name="userauthcodes",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="userauthcodes",
            name="expires_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]