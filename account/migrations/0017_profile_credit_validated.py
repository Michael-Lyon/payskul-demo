# Generated by Django 4.1.3 on 2023-06-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_profile_has_active_loan'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='credit_validated',
            field=models.BooleanField(default=False),
        ),
    ]
