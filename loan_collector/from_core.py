from core.models import Transaction, Loan
from core.utils import Okra
from account.models import OkraLinkedUser
from django.utils import timezone
from payskul.settings import PAYSKUL_ACCOUNT
import logging
from datetime import date, timedelta
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404

logger = logging.getLogger('okra_validator')

PAYMENT_RATE = 0.3 # 30% of the person's monthly salary

def get_current_date():
    return date.today()

def get_expired_loans():
    # Calculate the date one month ago from today
    one_month_ago = get_current_date() - timedelta(days=30)

    # Use Q objects to construct the filter
    expired_loans = Loan.objects.filter(Q(end_date__lt=one_month_ago) | Q(end_date__isnull=True))

    return expired_loans


def perform_loan_repayment(loan, charge, user, api_reference, api_status):
    # Create a new transaction
    transaction = Transaction.objects.create(
        loan=loan,
        reference=loan.reference,
        api_reference=api_reference,
        user=user,
        amount=charge,
        description="Loan repayment",
        status=api_status,
        type="FR"
    )

    if api_status == "success":
        # Update loan model
        loan.total_repayment += charge
        if loan.total_repayment >= loan.amount_to_pay_back:
            loan.cleared = True
        loan.save()
        transaction.save()
        # Perform any additional actions with the transaction data if needed
        # ...


def check_expired_loans():
    print("Hello")
    okra = Okra()
    # Get current datetime
    current_datetime = timezone.now()

    # Get loans with end_date earlier than current datetime and not cleared
    expired_loans = get_expired_loans()
    paystack_banks = Okra.paystack_banks()

    # Iterate over expired loans
    for loan in expired_loans:
        # Get the user of the loan
        user = loan.user

        # Check if the user has an account (nuban)
        okra_link = get_object_or_404(OkraLinkedUser, user=user)
        charge = (okra_link.avg_income * PAYMENT_RATE) # amount to charge the user

        if not okra_link.income_accounts:
            if okra.get_nuban_balances(okra_link.customer_id):
                # CHECK BALANCE IN EACH ACCOUNT 
                balances = okra_link.balance_ids.split(":") # THE ":" is a delimeter for all balance ids
                nubans = okra_link.income_accounts.split(":") # THE ":" is a delimeter for
                banks = okra_link.income_banks.split(":")
                # LOOP THROUGH EACH BALANCE TO MAKE A CHARGE ON ACCOUNT WITH SUFFICIENT BALANCE
                for i in range(len(balances)):
                    nuban = nubans[i]
                    balance = balances[i] 
                    bank = banks[i]

                    # Check for the corresponding bank in Paystack Api
                    bank_details = next((p_bank for p_bank in paystack_banks if p_bank['name'] == bank), None)

                    if bank_details:        
                        bal = okra.get_balance(balance_id=balance)
                        if bal >= charge:
                            api_data = okra._initiate_payment(nuban, okra_link.user, bank_details['code'], charge)
                
                            # Check if API call was successful
                            if api_data:
                                # Parse API response and extract necessary information
                                api_reference = api_data.get("ref")
                                api_status = api_data.get("status")

                                # Perform loan repayment if API call was successful
                                perform_loan_repayment(loan, charge, user, api_reference, api_status)
                            else:
                                logger.error("API call for loan repayment failed.")
                        else:
                            logger.warning("Insufficient balance for loan repayment.")
                    else:
                        logger.error("COLLECT LOAN: No Bank Match found for user", user)
            else:
                logger.warning("No nuban balances found for user", user)
