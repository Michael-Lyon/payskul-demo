import json
import requests
from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.models import OkraLinkedUser, Profile
from core.utils import Okra

from .models import Bank, Loan, PaymentSlip, SchoolBank, Transaction, Wallet, Card, Service, Service_Category
from .serializers import LoanSerializer, TransactionSerializer, WalletSerializer, CardSeriilizer, ServiceSerializer,ServiceCategorySerializer, DetailSerializer
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('okra_validator') 
User = get_user_model()


@csrf_exempt
@api_view(['Get'])
def validate_user_loan(request, *args, **kwargs):
    """Endpoint to certify that a user is eligible for loan facility access

     A get request to get that the user is eligible for loan facility access
    User would be identofied using JWT
    
    On success: {"message": "User validated successfully", "credit_limit": 10000}
    On fail: {"message": "An error occured please try again."}
    """
    can_borrow = False
    try:
        user = request.user
        if Loan.objects.filter(user=user).exists():
            can_borrow = False if Loan.objects.filter(user=user, cleared=False).exists() else True

        # link = OkraLinkedUser.objects.get(user=user)
        ok = Okra()
        customerId = user.linked_user.customer_id
        data = ok.update_customer_income_data(user, customerId)
        data["data"] = {"can_borrow":can_borrow}
        data["message"] = "User validated successfully"
        data["success"] = True
        return Response(data, status.HTTP_200_OK)
    except Exception as e:
            print(e)
            logger.exception("Exception Occured while validating user loan: " + str(e))
            data = { "success": False, "message": "An error occured please try again."}
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def apply_loan(request, *args, **kwargs):
    """Endpoint to apply for the users loan

    On POST request
        Keyword arguments:
        
        loan_details : {
            service -- what service is the user trying to apply for the loan the id of the service
            amount_needed -- how much does the user need?
            start_date -- when is this loan service active
            end_date -- when is this loan due
            amount_to_pay_back -- how much is the user supposed to pay back},
        
        bank_details : {
            receivers_name -- who is to recieve the money
            bank_name -- from the list of bank from the get bank api,
            bank_account_number -- acccount for the money to be paid into
            description -- description of the payment
            amount -- amount to be paid into the bank account
        }

        auth : {
            pin: user transaction pin
        }
    """
    user = request.user
    method = request.method
    profile = request.user.profile
    can_borrow = False

    if Loan.objects.filter(user=user).exists():
        can_borrow = False if Loan.objects.filter(user=user, cleared=False).exists() else True

    if method == "POST":
        loan_data = request.data["loan_details"]
        bank_data = request.data["bank_details"]
        auth_data = request.data["auth"]
        limit = OkraLinkedUser.objects.get(user=request.user).initial_limit

        # Validate user transaction pin
        if profile.pin == auth_data['pin']:
            del request.data['auth']
            if not can_borrow:
                return Response({"message": "This user has an outstanding loan."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the loan amount is valid and add it to the database
            if loan_data["amount_needed"] > limit:
                return Response({"status": False, "message": "Loan amount exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

            # Save loan to Loan model
            serializer = LoanSerializer(data=loan_data)
            if serializer.is_valid():
                # Add loan amount to wallet
                if Wallet.objects.filter(user=user).exists():
                    wallet = Wallet.objects.get(user=user)
                    wallet.amount += loan_data["amount_needed"]
                    wallet.save()

                # Save the loan if everything is good
                loan = serializer.save(user=request.user)
                transaction = None
                # Create a transaction for fee payment
                try:
                    transaction = Transaction.objects.create(
                        user=request.user,
                        loan=loan,
                        description=bank_data["description"],
                        type="SFP",
                        amount=bank_data["amount"],
                    )
                except Exception as e:
                    print("Error")
                    return Response({"status": False, "message": "Error creating transaction"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    # Subtract the bank_amount from the amount in wallet
                    wallet.amount -= bank_data["amount"]
                    wallet.save()

                    # Create the school bank and payment slip
                    school = SchoolBank.objects.create(
                        bank_name=bank_data["bank_name"],
                        account_number=bank_data["bank_account_number"],
                    )

                    PaymentSlip.objects.create(
                        user=request.user,
                        amount=bank_data["amount"],
                        school=school,
                        reference=transaction.reference,
                    )

                    return Response({"status": True, "message": "Loan applied successfully"},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response({"status": False, "message": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": False, "message": "Invalid pin"},
                            status=status.HTTP_401_UNAUTHORIZED)

# @csrf_exempt
@api_view(['GET'])
def get_banks(request, *args, **kwargs):
    data = Okra.bank_list()
    return Response(data)


@api_view(["GET", ])
def update_client_income_status(request, *args, **kwargs):
    try:
        user = request.user
        link = OkraLinkedUser.objects.get(user=user)
        ok = Okra()
        customerId = user.linked_user.customer_id
        data = ok.update_customer_income_data(user, customerId)

        return Response(data, status=ok)
    except Exception as e:
            print(e)
            return Response({"message": "An error occured please try again."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

# @csrf_exempt
@api_view(['GET'])
def loan_list(request, pk=None, *args, **kwargs):
    queryset = Loan.objects.filter(user=request.user)
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

from django.http import HttpResponse

# @csrf_exempt
def read_file(request):
    f = open('warning.log', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")



@method_decorator(csrf_exempt, name='dispatch')
class TransactionListCreateView(generics.ListAPIView):
    """ Create or list transactions for a given user.

    A GET request to list all transactions for a given user.

    POST request:
        'amount',
        'description',
        'type' is one of these FR/WT  [('FR', 'Fee Repayment'),('WT', 'Wallet Top Up'),]
        'loan', loan id the repayment 
        'my_total_payments'
    """

    # queryset = Transaction.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user) 
    
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
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
    
    serializer_class = WalletSerializer


class ServiceListCreateView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceCategoryListCreateView(generics.ListAPIView):
    queryset = Service_Category.objects.all()
    serializer_class = ServiceCategorySerializer


@method_decorator(csrf_exempt, name='dispatch')
class CardListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
    
    serializer_class = CardSeriilizer
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        return serializers.ValidationError("Something went wrong")


class DetailListView(generics.ListAPIView):
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    serializer_class = DetailSerializer


@csrf_exempt
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
    user = authenticate(request, username=request.user.username, password=raw_data['pin'])
    if user:
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


@csrf_exempt
@api_view(['POST'])
def webhook_view(request):
    if request.method == 'POST':
        # Get the payload sent by the webhook
        payload = request.body
        okra = Okra()
        status = okra.validate_update_user_status(payload=payload)
        print(status)
        return HttpResponse(status=200)
    else:
        payload = json.loads(request.body)
        print(payload)
        return HttpResponse(status=200)
