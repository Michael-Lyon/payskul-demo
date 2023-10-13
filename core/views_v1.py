import json
import requests
from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from account.models import OkraLinkedUser, Profile, SensitiveData
from account.utils import check_hashed_value
from okra_utils.utils2 import Okra

from .models import Bank, Loan, PaymentSlip, SchoolBank, Transaction, Wallet, Card, Service, Service_Category
from .serializers import LoanSerializer, TransactionSerializer, WalletSerializer, CardSeriilizer, ServiceSerializer,ServiceCategorySerializer, DetailSerializer
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from dotenv import load_dotenv
import os
# import the logging library
import logging
from django.http import HttpResponse
import traceback
from django.db import transaction as _transaction

# Get an instance of a logger
logger = logging.getLogger('okra_validator')
User = get_user_model()
load_dotenv()

@csrf_exempt
@api_view(['Get'])
def validate_user_loan(request, *args, **kwargs):
    """Endpoint to certify that a user is eligible for loan facility access

    A get request to get that the user is eligible for loan facility access
    User would be identofied using JWT

    On success: {"message": "User validated successfully", "credit_limit": 10000}
    On fail: {"message": "An error occured please try again."}
    """
    # TODO: ADD A CHECK TO KNNOW IF IT'S A FIRST TIME OR SECIND TIME
    can_borrow = False
    try:
        user = request.user
        if Loan.objects.filter(user=user).exists():
            can_borrow = False if Loan.objects.filter(user=user, cleared=False).exists() else True
        if OkraLinkedUser.objects.filter(user=user).exists():
        # link = OkraLinkedUser.objects.get(user=user)
            ok = Okra()
            credit_limit = OkraLinkedUser.objects.get(user=user).initial_limit
            # data = ok.update_customer_income_data(user, customerId)
            data = {}
            data["can_borrow"]= can_borrow
            data["message"] = "User validated successfully"
            data["status"] = True
            data['credit_limit'] = credit_limit
            return Response(data, status.HTTP_200_OK)
        return Response({"message":"Unable to validate user", "status":False, "can_borrow": False, "credit_limit": 0}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        logger.exception("Exception Occured while validating user loan: " + str(e))
        data = { "success": False, "message": "An error occured please try again."}
        return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['POST'])
def confirm_okra_link(request):
    if request.method == 'POST':
        user = request.user
        # Get the payload sent by the webhook
        payload = request.data
        okra = Okra()
        try:
            data = okra.validate_update_user_status(payload=payload, user=user)
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"An error occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        payload = json.loads(request.body)
        print(payload)
        return HttpResponse(status=200)



@api_view(['POST'])
def apply_loan(request, *args, **kwargs):
    """Endpoint to apply for a loan."""
    user = request.user
    method = request.method

    if method == "POST":
        try:
            loan_data = request.data["loan_details"]
            limit = OkraLinkedUser.objects.get(user=user).initial_limit
            loan_data["amount_needed"] = Decimal(loan_data["amount_needed"])
            loan_data["amount_to_pay_back"] = Decimal(loan_data["amount_to_pay_back"])

            # Check if the user has outstanding loans
            if Loan.objects.filter(user=user, cleared=False).exists():
                return Response({"message": "This user has an outstanding loan."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the loan amount is valid
            if loan_data["amount_needed"] > limit:
                return Response({"status": False, "message": "Loan amount exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the loan if everything is good
            serializer = LoanSerializer(data=loan_data)
            if serializer.is_valid():
                serializer.save(user=user)
                # Add loan amount to the wallet if it exists
                if Wallet.objects.filter(user=user).exists():
                    wallet = Wallet.objects.get(user=user)
                    wallet.amount += loan_data["amount_needed"]
                    wallet.save()
                Transaction.objects.create(
                    loan=serializer.instance,
                    user=user,
                    amount=serializer.instance.amount_needed,
                    status='success',
                    type="LN",
                )
                return Response({"status": True, "message": "Loan applied successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"status": False, "message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_slip(request, *args, **kwargs):
    """
    Endpoint to apply for the user's loan.

    On POST request:
    {
        - schoool_details: {
            "recipient": "Name of  sender",
            "school_name": "Name of the school",
            "school_address": " address of the school",
        }

        - bank_details: {
            "bank_name": "Name of the bank",
            "bank_account_number": "Account number",
            "description": "Description of the payment",
            "amount": "Amount to be paid into the bank account"
        },

        - auth: {
            "pin": "User transaction pin"
        }
    }
    """
    user = request.user
    method = request.method
    profile = user.sensitive
    wallet = Wallet.objects.get(user=user)

    if method == "POST":
        bank_data = request.data.get("bank_details", {})
        auth_data = request.data.get("auth", {})
        school_data = request.data.get("school_details", {})

        # Validate user transaction pin
        if profile.pin == str(auth_data.get('pin')):
            try:
                # Get the latest uncleared loan
                with _transaction.atomic():
                    loan = Loan.objects.filter(user=user, cleared=False).latest('start_date')
                    payment_amount = Decimal(bank_data.get("amount", 0))

                    # Subtract the bank_amount from the amount in the wallet
                    # TODO: Validate banks
                    if wallet.amount >= payment_amount:
                        school, created = SchoolBank.objects.get_or_create(
                            name=school_data.get("school_name"),
                            address=school_data.get("school_address"),
                            bank_name=bank_data.get("bank_name"),
                            account_number=bank_data.get("bank_account_number"),
                        )
                        # Create a transaction for fee payment
                        transaction = Transaction.objects.create(
                            user=user,
                            loan=loan,
                            description=bank_data.get("description", ""),
                            type="SFP",
                            amount=Decimal(payment_amount),
                        )

                        PaymentSlip.objects.create(
                        recipient=school_data.get("recipient", ""),
                        user=user,
                        amount=payment_amount,
                        school=school,
                        description=bank_data.get("description"),
                        reference=transaction.reference,
                        )

                        wallet.amount = wallet.amount - payment_amount
                        wallet.save()

                        return Response({"status": True, "message": "Payment applied successfully", "balance": wallet.amount}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status": False, "message": f"Transaction Amount Surpassed loaned amount"}, status=status.HTTP_400_BAD_REQUEST)
            except Loan.DoesNotExist:
                return Response({"status": False, "message": "No uncleared loan found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(e)
                traceback.print_exc()
                return Response({"status": False, "message": "Error creating transaction"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"status": False, "message": "Invalid pin"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"status": False, "message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
        customerId = link.customer_id
        data = ok.update_customer_income_data(user, customerId)
        data["message"] = "Client updated successfully"
        data["status"] = True
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
            print(e)
            return Response({"message": "An error occured please try again."}, status.HTTP_500_INTERNAL_SERVER_ERROR)


# @csrf_exempt
@api_view(['GET'])
def loan_list(request):
    # get the users latest loan
    if Loan.objects.filter(user=request.user).exists():
        queryset = Loan.objects.filter(user=request.user, cleared=False).latest('start_date')
        # queryset = Loan.objects.filter(user=request.user)
        data = LoanSerializer(queryset).data
        return Response({"status": True, "data":data}, status=status.HTTP_200_OK)
    else:
        return Response({"status": True, "data": {
                "service" : None,
                "amount_needed" : 0,
                "start_date" : None,
                "end_date" : None,
                "amount_to_pay_back" : 0,
                "total_repayment" : 0,
                "cleared" : None
        }}, status=status.HTTP_200_OK)


# @csrf_exempt
def read_file(request):
    f = open('warning.log', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")



class TransactionListCreateView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get(self, request):
        user = request.user
        paginator = PageNumberPagination()
        paginator.page_size = 4  # You can adjust the page size as needed
        transactions = Transaction.objects.filter(user=user).order_by('-date')
        result_page = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(result_page, many=True, context={"request":request})

        loan = Loan.get_loan(self.request.user)
        total_loan_payments = loan.total_repayment if loan else 0
        total_fees_paid =Transaction.get_total_fees_paid(self.request.user)


        data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            'total_fees_paid': total_fees_paid,
            'total_loan_repayment': total_loan_payments,
            'results': serializer.data,
        }
        return Response(data)



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
def webhook_view(request):
    if request.method == 'POST':
        user = request.user
        print(user)
        # Get the payload sent by the webhook
        payload = request.data
        okra = Okra()
        try:
            data = okra.validate_update_user_status(payload=payload, user=user)
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"An error occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        payload = json.loads(request.body)
        print(payload)
        return HttpResponse(status=200)


def link_account_okra_test(request):
    return render(request, 'core/demo.html')


class ExtendLoanView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        date = request.data.get('date')
        pin = request.data.get('pin')
        sensitive_data = SensitiveData.objects.get(user=request.user)

        if check_hashed_value(pin, sensitive_data.transaction_pin_hash,):
            return Response({"status":False,'message': 'Invalid Pin'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            loan = Loan.get_loan(user=request.user)
            loan.end_date = date
            loan.save()
        except Loan.DoesNotExist:
            return Response({"status":False,'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        finally:
            if not loan:
                return Response({"status":False,'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)


        return Response({"status":True,'message': 'Loan extended successfully'}, status=status.HTTP_200_OK)

class LoanRepaymentView(APIView):
    authentication_classes = [JWTAuthentication]
    PAYSTACK_SECRET = os.getenv("PAYSATCK_SECRET")
    PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"

    PAYSTACK_HEADERS = {
        "accept": "application/json; charset=utf-8",
        "content-type": "application/json",
        "authorization": f"Bearer {PAYSTACK_SECRET}"
    }

    def post(self, request):
        amount_paid = request.data.get('amount_paid')
        reference_id = request.data.get('reference_id')

        try:
            loan = Loan.get_loan(user=request.user)
        except Loan.DoesNotExist:
            return Response({'message': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

        response = requests.get(
            url=f"{self.PAYSTACK_VERIFY_URL}{reference_id}",
            headers=self.PAYSTACK_HEADERS
        ).json()

        if response.get('status') == True:
            amount = response['data']['amount']
            loan.total_repayment += amount
            loan.save()

            transaction = Transaction.objects.create(
                user=request.user,
                loan=loan,
                api_reference=response['data']['reference'],
                amount=amount,
                status="success",
                type='FR',
                description='Loan Repayment'
            )
            transaction.save()

            if loan.amount_to_pay_back == loan.total_repayment:
                loan.cleared = True
                loan.save()
            return Response({'message': 'Success!'}, status=status.HTTP_200_OK)
        else:
            transaction = Transaction.objects.create(
                user=request.user,
                loan=loan,
                amount=amount_paid,
                status="failed",
                type='FR',
                description='Loan Repayment'
            )
            transaction.save()
            return Response({'message': 'Transaction Failed!'}, status=status.HTTP_400_BAD_REQUEST)

class ReferralView(APIView):
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        my_refs = profile.get_recommened_profiles()

        return Response({'referrals':my_refs}, status=status.HTTP_200_OK)
