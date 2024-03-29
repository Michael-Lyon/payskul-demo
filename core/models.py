from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from rest_framework.authtoken.models import Token
from django.db.models import Sum
import uuid
from account.models import Profile

User = get_user_model()


class Service_Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
   
    class Meta:
        ordering = ('name',)
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self) -> str:
        return self.name



class Service(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    service_category = models.ForeignKey(Service_Category, default=1, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    deposit_rate = models.DecimalField(max_digits=5, default=0, decimal_places=2)
    description = models.CharField(max_length=100, default="Demo")

    
    class Meta:
        ordering = ('name',)
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self) -> str:
        return f"{self.name} with a down payment of {self.deposit_rate}"


class SchoolBank(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"School: {self.name} Bank Name: {self.bank_name} Account: {self.account_number} verified: {self.verified}"


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan", blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    amount_needed = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    amount_to_pay_back = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    total_repayment = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)
    cleared = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-start_date',)
        verbose_name = "Loan"
        verbose_name_plural = "Loans"


    def clean(self):
        if self.user and not self.cleared:
            existing_loan = Loan.objects.filter(user=self.user, cleared=False).exists()
            if existing_loan:
                raise ValidationError("User already has an existing uncleared loan.")
        super().clean()

    def __str__(self) -> str:
        return f"{self.user } on loan of {self.amount_needed}  from {self.start_date} to {self.end_date}"

    @classmethod
    def get_loan(self, user):
        return Loan.objects.get(user=user, cleared=False) if Loan.objects.filter(user=user, cleared=False).exists() else None

class PaymentSlip(models.Model):
    """
    This model is used to store information about payments and once
    they are approved, the payment would be made.
    and the status would be updated accordingly.
    """

    PAYMENT_CHOICES = (
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
        ("approved", "Approved"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_slip")
    recipient = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    description = models.TextField(blank=True, max_length=200, null=True)
    school = models.ForeignKey(SchoolBank, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="pending")
    reference = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"Payment Slip for "

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('FR', 'Fee Repayment'),
        ('SFP', 'Fees Paid'),
        ('LN', 'Wallet Top Up'),
    ]
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
        ('success', 'Success'),
    ]
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='loan_transaction', blank=True, null=True)
    reference = models.CharField(max_length=30, blank=True, null=True)
    api_reference = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, default=0.0, decimal_places=2)
    description = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, default="pending", choices=TRANSACTION_STATUS_CHOICES)
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES, default='WT')


    def get_total_payments(self):
        loan = Loan.get_loan(self.user)
        if loan == None:
            return 0
        total = Transaction.objects.filter(loan=loan, user=self.user, type="FR").aggregate(Sum('amount'))
        return total['amount__sum'] or 0 if not total["amount__sum"] else total["amount__sum"]


    @classmethod
    def get_total_fees_paid(cls, user):
        total_fees_paid = cls.objects.filter(user=user, type="SFP", status="succeeded").aggregate(Sum('amount'))
        return total_fees_paid['amount__sum'] or 0

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = str(uuid.uuid4())[:30]  # Generate a UUID reference
        super().save(*args, **kwargs)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="card", blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    cvv = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
    def __str__(self):
        return f"Card for {self.user}"
