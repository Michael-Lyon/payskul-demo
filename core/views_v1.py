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

from account.models import OkraLinkedUser, Profile
from okra_utils.utils2 import Okra

from .models import Bank, Loan, PaymentSlip, SchoolBank, Transaction, Wallet, Card, Service, Service_Category
from .serializers import LoanSerializer, TransactionSerializer, WalletSerializer, CardSeriilizer, ServiceSerializer,ServiceCategorySerializer, DetailSerializer
from rest_framework import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
# import the logging library
import logging
from django.http import HttpResponse


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
                return Response({"status": True, "message": "Loan applied successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"status": False, "message": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @csrf_exempt
# @api_view(['POST'])
# def apply_loan(request, *args, **kwargs):
#     """Endpoint to apply for the users loan

#     On POST request
#         Keyword arguments:


#         loan_details: {
#             service -- what service is the user trying to apply for the loan the id of the service
#             amount_needed -- how much does the user need?
#             start_date -- when is this loan service active
#             end_date -- when is this loan due
#             amount_to_pay_back -- how much is the user supposed to pay back
#         }


#     """
#     user = request.user
#     method = request.method
#     can_borrow = False

#     if Loan.objects.filter(user=user).exists():
#         can_borrow = False if Loan.objects.filter(user=user, cleared=False).exists() else True

#     if method == "POST":
#         loan_data = request.data["loan_details"]
#         limit = OkraLinkedUser.objects.get(user=request.user).initial_limit

#         # Validate user transaction pin
#         if not can_borrow:
#             return Response({"message": "This user has an outstanding loan."}, status=status.HTTP_400_BAD_REQUEST)

#         # Check if the loan amount is valid and add it to the database
#         if loan_data["amount_needed"] > limit:
#             return Response({"status": False, "message": "Loan amount exceeds limit"}, status=status.HTTP_400_BAD_REQUEST)

#         # Save loan to Loan model
#         serializer = LoanSerializer(data=loan_data)
#         if serializer.is_valid():
#             # Add loan amount to wallet
#             if Wallet.objects.filter(user=user).exists():
#                 wallet = Wallet.objects.get(user=user)
#                 wallet.amount += loan_data["amount_needed"]
#                 wallet.save()

#             # Save the loan if everything is good
#             serializer.save(user=request.user)

#             return Response({"status": True, "message": "Loan applied successfully"},
#                                 status=status.HTTP_201_CREATED)
#         else:
#             return Response({"status": False, "message": serializer.errors},
#                             status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_slip(request, *args, **kwargs):
    """
    Endpoint to apply for the user's loan.

    On POST request:
        - bank_details: {
            "receivers_name": "Name of the receiver",
            "bank_name": "Name of the bank",
            "bank_account_number": "Account number",
            "description": "Description of the payment",
            "amount": "Amount to be paid into the bank account"
        }

        - auth: {
            "pin": "User transaction pin"
        }
    """
    user = request.user
    method = request.method
    profile = user.profile
    wallet = Wallet.objects.get(user=user)

    if method == "POST":
        bank_data = request.data.get("bank_details", {})
        auth_data = request.data.get("auth", {})

        # Validate user transaction pin
        if profile.pin == auth_data.get('pin'):
            try:
                # Get the latest uncleared loan
                loan = Loan.objects.filter(user=user, cleared=False).latest('start_date')

                # Create a transaction for fee payment
                transaction = Transaction.objects.create(
                    user=user,
                    loan=loan,
                    description=bank_data.get("description", ""),
                    type="SFP",
                    amount=bank_data.get("amount", 0),
                )

                # Subtract the bank_amount from the amount in the wallet

                wallet.amount -= transaction.amount
                wallet.save()

                # Create the school bank and payment slip
                school, created = SchoolBank.objects.get_or_create(
                    bank_name=bank_data.get("bank_name", ""),
                    account_number=bank_data.get("bank_account_number", ""),
                )

                PaymentSlip.objects.create(
                    receivers_name=bank_data.get("receivers_name", ""),
                    user=user,
                    amount=transaction.amount,
                    school=school,
                    reference=transaction.reference,
                )

                return Response({"status": True, "message": "Payment applied successfully"}, status=status.HTTP_201_CREATED)
            except Loan.DoesNotExist:
                return Response({"status": False, "message": "No uncleared loan found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
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
        data = LoanSerializer(queryset, many=True).data
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



@method_decorator(csrf_exempt, name='dispatch')
class TransactionListCreateView(generics.ListAPIView):
    # queryset = Transaction.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user) 



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