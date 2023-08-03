from django.contrib import admin
from django.contrib import admin
from .models import Transaction, PaymentSlip
from .utils import Okra
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

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "service_category", "deposit_rate")

    def service_category(self, obj):
        category = Service_Category.objects.get(id=obj.service_category.id)
        return category.name
    
    service_category.short_description = "Service Category"

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")

class SchoolBankAdmin(admin.ModelAdmin):
    list_display = ("name", "bank_name", "account_number", "verified")

class LoanAdmin(admin.ModelAdmin):
    list_filter = ("service", "cleared")
    list_display = ("get_first_name", "get_last_name", "service", "amount_needed", "start_date", "end_date", "amount_to_pay_back", "total_repayments", "cleared", "updated")

    def get_first_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.first_name
    
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.last_name
    
    get_last_name.short_description = "Last Name"

    def service(self, obj):
        service = Service.objects.get(id=obj.service.id)
        return service.name
    
    service.short_description = "Service"

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("reference", "api_reference", "date")
    list_filter = ("status", "type")
    search_fields = ("reference__icontains", "api_reference__icontains")

class WalletAdmin(admin.ModelAdmin):
    list_display = ("get_first_name", "get_last_name")

    def get_first_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.first_name
    
    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        name = User.objects.get(id=obj.user.id)
        return  name.last_name
    
    get_last_name.short_description = "Last Name"




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