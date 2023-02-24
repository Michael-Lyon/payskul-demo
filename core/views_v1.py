from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Bank, Loan, Transaction, Wallet, Card, Service, Service_Category
from .serializers import LoanSerializer, TransactionSerializer, WalletSerializer, CardSeriilizer, ServiceSerializer, ServiceCategorySerializer
from .utils import validate_bvn, validate_national_id, generate_random_credit
from rest_framework import serializers


@api_view(['POST'])
def validate_user_loan(request, *args, **kwargs):
    """Endpoint to certify that a user is eligible for loan facility access

    Keyword arguments:
    fullname -- user full name
    home_address -- user home address
    bvn -- user bank verification number
    nin -- user national identity number
    phone_number -- user phone number
    account_number -- user bank account number
    account_name -- user bank account name
    bank_name -- user bank name
    pin -- user pin

    Return:  {'meaage': True / False} if user is eligible or not
    """

    if request.user.is_authenticated:
        raw_data = request.data
        profile = request.user.profile
        if not (profile.verified):
            try:
                limit = generate_random_credit()
                if limit <= 25_000:
                    return Response({"message": "User has a low credit limit", })
                nin = raw_data['nin']
                bvn = raw_data['bvn']
                if validate_bvn(bvn) and validate_national_id(nin):
                    profile.credit_limit = limit
                    profile.nin = nin
                    profile.verified = True
                    profile.save()
                    if not Bank.objects.filter(user=request.user).exists():
                        bank = Bank.objects.create(
                            user=request.user,
                            name=raw_data['bank_name'],
                            account_number=raw_data['account_number'],
                            account_name=raw_data['account_name'],
                            bvn=bvn
                        )
                        bank.save()
                    return Response({"message": "User validated successfully", })
                else:
                    return Response({"message": "Bvn and or Nin not valid", })
            except Exception as e:
                print(e)
                return Response({"message": "An error occured please try again."})
        return Response({"message": "User has already been verified!"})
    else:
        return Response({"message": "User is not authenticated! Login and try again"})


@api_view(['GET', 'POST'])
def apply_loan(request, *args, **kwargs):
    """Endpoint to apply for the users loan
    On GET request
        Returns the user {message: "User credit limit", data: {credit_limit: 100_000}}        

    On POST request
        Keyword arguments:
        service -- what service is the user trying to apply for the loan the id of the service
        down_payment -- how much is the down payment supposed to be
        amount_needed -- how much does the user need?
        start_date -- when is this loan service active
        end_date -- when is this loan due
        amount_to_pay_back -- how much is the user supposed to pay back

        Return:  {'message': True / False} if user is eligible or not
    """
    user = request.user
    method = request.method
    profile = request.user.profile
    if Loan.objects.filter(user=user).exists():
        can_borrow = True if Loan.objects.filter(user=user, cleared=True) else False
    else:
        can_borrow = True

    if method == 'GET':
        credit_limit = profile.credit_limit

        return Response({"message": "User credit limit status", 'data': {
            'credit_limit': credit_limit,
            'can_borrow': can_borrow
        }}, status=200)

    if method == "POST":
        if profile.pin == request.data['pin']:
            del request.data['pin']
            if not can_borrow:
                return Response({"message": "This user has an outstanding loan."})
            serializer = LoanSerializer(data=request.data)
            if serializer.is_valid():

                # Remove the down_payment amount fromt he users wallet
                if Wallet.objects.filter(user=user).exists():  # check if the user has a wallet
                    wallet = Wallet.objects.get(user=user)
                    amount = wallet.amount

                    # if user has less 0 in wallet then user is broke
                    if amount <= 0 or amount < serializer.validated_data['down_payment']:
                        return Response({"message": "User has no/insufficient money in wallet"})
                    amount -= Decimal(serializer.validated_data['down_payment'])
                else:
                    return Response({"message": "User has no wallet"})

                # Save the loan if everything is good
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Invalid pin"})



@api_view(['GET'])
def loan_list(request, pk=None, *args, **kwargs):
    queryset = Loan.objects.all()
    if request.method == 'GET':
        if pk is not None:
            # detail view
            # raise a 404 if not exists
            obj = get_object_or_404(Loan, pk=pk)
            data = LoanSerializer(obj, many=False)
            return Response(data)
        # list view
        data = LoanSerializer(queryset, many=True).data
        return Response(data)



class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        """
        Check the transaction so that to be able to monitor if the user is trying to payback the loan he took.
        """

        type = serializer.validated_data.get('type', None)
        # Check that the user is trying to re-pay his debt
        if type == "FR":
            repayment_amount = serializer.validated_data.get('amount', None)
            loan_id = serializer.validated_data.get('loan', None)

            # Find the loan instance with the given ID
            loan = Loan.objects.get(id=loan_id)

            # Update the total repayment amount for the loan
            loan.total_repayment += repayment_amount
            loan.save()

            # Check if the loan has been fully repaid
            if loan.total_repayment == loan.amount_needed:
                # Mark the loan as cleared
                loan.cleared = True
                loan.save()
        serializer.save(user=self.request.user)


class WalletListCreateView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class ServiceListCreateView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceCategoryListCreateView(generics.ListAPIView):
    queryset = Service_Category.objects.all()
    serializer_class = ServiceCategorySerializer


class CardListCreateView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSeriilizer


@api_view(['POST'])
def top_wallet(request, *args, **kwrgs):
    """To Top up the user wallet

    Args:
        id: id of the card the user is trying to make the top up from
        amount: amount the user wants to add to wallet
        pin: user transaction pip

    Returns:
        message: Success or Failed
    """
    rand_amount = generate_random_credit()
    raw_data = request.data
    pk=raw_data['id']
    to_withdraw = raw_data.get('amount')
    profile = request.user.profile
    if not Card.objects.filter(user=profile.user).exists():
        return Response({"message":"User has no existing card"})
    if raw_data['pin'] == profile.pin:
        card = get_object_or_404(Card, id=pk)
        amount = rand_amount - to_withdraw
        if amount > 0:
            wallet = card.user.wallet
            wallet.amount += Decimal(amount)
            wallet.save()
            Transaction.objects.create(
                user=card.user,
                amount=to_withdraw,
                status='Complete',
                type='WT',
            )
            return Response({'message': 'Charge successful'})
        return Response({'message': 'Insufficeint Funds'})
    return Response({'message': 'Pin incorrect.'})
