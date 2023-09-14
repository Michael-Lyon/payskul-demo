# Generated by Django 4.1.3 on 2023-09-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_alter_transaction_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("cancelled", "Cancelled"),
                    ("failed", "Failed"),
                    ("success", "Success"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
