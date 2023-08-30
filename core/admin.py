from django.contrib import admin
from django.contrib import admin
from .models import Transaction, PaymentSlip
from okra_utils.utils import Okra
from payskul.settings import PAYSKUL_ACCOUNT
from . models import *
from django.core.mail import send_mail
from payskul.settings import EMAIL_HOST_USER as SENDER
# Register your models here.
admin.site.register(Service)
admin.site.register(Service_Category)
admin.site.register(Transaction)
admin.site.register(Bank)
admin.site.register(Wallet)
admin.site.register(Loan)
admin.site.register(Card)
admin.site.register(SchoolBank)





def send(status: str, reference: str, email: str):
    send_mail(
            "PaySkul School Fee Payment", f"Your payment for {reference} is {status}", 
            from_email=SENDER, recipient_list=[email], fail_silently=False
            )



def initiate_payment_and_update_models(modeladmin, request, queryset):
    """
    This function is an admin function where an admin asfter verifying a school can initiate 
    transaction for a user to pay school fee. And all related models would be updated 
    accordingly. Where a transaction failed or gets cancelled, all aount would be added back
    to the user wallet and the user would need to intiate the transaction again.
    they would be notified through email.
    """
    for payment_slip in queryset:
        # Initiate payment
        okra = Okra()
        result = okra._initiate_payment(PAYSKUL_ACCOUNT, payment_slip.school.account_number, payment_slip.amount)
        transaction = transaction.objects.get(reference=payment_slip.reference)
        transaction.api_reference = result["ref"]
        wallet = Wallet.objects.get(user=transaction.user)
        
        if result["status"] == "success":
            payment_slip.status = "success"
            transaction.status = "success"
            send(result["status"], transaction.reference, payment_slip.user.email)

        elif result["status"] == "cancelled":
            send(result["status"], transaction.reference, payment_slip.user.email)
            payment_slip.status = "cancelled"
            transaction.status = "cancelled"
            wallet += transaction.amount
            send(result["status"], transaction.reference, payment_slip.user.email)

        elif result["status"] == "failed":
            send(result["status"], transaction.reference, payment_slip.user.email)
            payment_slip.status = "failed"
            transaction.status = "failed"
            wallet = Wallet.objects.get(user=transaction.user)
            wallet += transaction.amount
            send(result["status"], transaction.reference, payment_slip.user.email)

        transaction.save()
        payment_slip.save()
        wallet.save()


initiate_payment_and_update_models.short_description = "Initiate Payment and Update Models"


class PaymentSlipAdmin(admin.ModelAdmin):
    list_display = [
        "user", "amount", "school", "status"
    ] 
    actions = [initiate_payment_and_update_models]

admin.site.register(PaymentSlip, PaymentSlipAdmin)