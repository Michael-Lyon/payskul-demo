from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from account.models import Profile

User = get_user_model()


class Service_Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
   
    class Meta:
        ordering = ('name',)
        verbose_name = "Service Category"
        verbose_name_plural = "Services Category"

    def __str__(self) -> str:
        return self.name



class Service(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    service_category = models.ForeignKey(Service_Category, default=1, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    deposit_rate = models.DecimalField(max_digits=5, default=0, decimal_places=2)
    decription = models.CharField(max_length=100, default="Demo")

    
    class Meta:
        ordering = ('name',)
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self) -> str:
        return f"{self.name} with a down payment of {self.deposit_rate}"



class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    down_payment = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    amount_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    amount_to_pay_back = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_repayment = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    cleared = models.BooleanField(default=False)

    class Meta:
        ordering = ('-start_date',)
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self) -> str:
        return f"{self.user } on loan of {self.amount_needed}  from {self.start_date} to {self.end_date}"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('LO', 'Loan'),
        ('FR', 'Fee Repayment'),
        ('WT', 'Wallet Top Up'),
    ]
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_transaction', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES, default='WT')
    




class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank")
    name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bvn = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def __str__(self) -> str:
        return f"{self.user } --> {self.name}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet", blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)

    def __str__(self) -> str:
        return f"{self.user } --> {self.amount} in wallet"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="card")
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    cvv = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        
    def __str__(self):
        return f"Card for {self.user}"