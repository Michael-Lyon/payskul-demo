# Generated by Django 4.1.3 on 2022-12-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_transaction_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="status",
            field=models.CharField(default="Pending", max_length=20),
        ),
    ]