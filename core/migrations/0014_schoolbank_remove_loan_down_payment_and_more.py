# Generated by Django 4.1.3 on 2023-07-07 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_alter_card_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='loan',
            name='down_payment',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('FR', 'Fee Repayment'), ('SFP', 'School Fees Payment')], default='WT', max_length=3),
        ),
        migrations.CreateModel(
            name='PaymentSlip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('cancelled', 'Cancelled'), ('approved', 'Approved'), ('succeeded', 'Succeeded'), ('failed', 'Failed')], max_length=20)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.schoolbank')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_slip', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
