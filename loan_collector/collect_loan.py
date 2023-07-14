from core.models import Transaction, Loan
from core.utils import Okra
from account.models import OkraLinkedUser
from django.utils import timezone
from payskul.settings import PAYSKUL_ACCOUNT

PAYMENT_RATE = 0.3 # 30% of the person montly salary
def check_expired_loans():
    print("Hello")
    okra = Okra()
    # Get current datetime
    current_datetime = timezone.now()

    # Get loans with end_date earlier than current datetime and not cleared
    expired_loans = Loan.objects.filter(end_date__lt=current_datetime, cleared=False)

    # Iterate over expired loans
    for loan in expired_loans:
        # Get the user of the loan
        user = loan.user

        #  check if the user has an account(nuban)
        okra_link = OkraLinkedUser.objects.get(user=user)
        charge = (okra_link.avg_income * (30 / 100)) # amount to charge the user
        if not okra_link.income_accounts:
            if okra.get_nuban_balances(okra_link.customer_id):
                # CHECK BALANCE IN EACH ACCOUNT 
                balances = okra_link.balance_ids.split(":") # THE ":" is a delimeter for all balance ids
                nubans = okra_link.income_accounts.split(":") # THE ":" is a delimeter for
                banks = okra_link.income_banks.split(":")
                # LOOP THROOUGH EACH BALANCE TO MAKE A CHARGE ON ACCOUNT WITH SUFFICIENT BALANCE
                for i in range(len(balances)):
                    nuban = nubans[i]
                    balance = balances[i] 
                    bank = banks[i]
                    bal = okra.get_balance(balance_id=balance)
                    if bal >= charge:
                        api_data = okra._initiate_payment(nuban, okra_link.user, bank, charge)
            
                    # Check if API call was successful
                        # Parse API response and extract necessary information
                        api_reference = api_data.get("ref")
                        api_status = api_data.get("status")

                        # Create a new transaction
                        transaction = Transaction.objects.create(
                            loan=loan,
                            reference=loan.reference,
                            api_reference=api_reference,
                            user=loan.user,
                            date=current_datetime,
                            amount=charge,
                            description="Loan repayment",
                            status=api_status,
                            type="FR"
                        )

                        if api_status == "success":
                        # Update loan model
                            loan.total_repayment += charge
                            if loan.total_repayment == loan.amount_to_pay_back:
                                loan.cleared = True
                        # loan.cleared = True
                        loan.save()
                        transaction.save()
                        # Perform any additional actions with the transaction data if needed
                        # ...