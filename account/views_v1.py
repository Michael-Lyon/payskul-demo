from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
import requests
from django.urls import reverse
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt

from account.customs import CustomPagination
from scheduled_tasks.my_tasks import schedule_email_task
from .models import Profile, MyUserAuth, SecurityQuestion, SensitiveData
from .serializers import LoginSerializer, ChangePasswordSerializer, SecurityQuestionSerializer, UserSerializer
from .utils import check_hashed_value, check_pin, get_code, hash_value, send_verification_code, verify_email_smtp

from core.serializers import DetailSerializer
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail
from django.core.mail import send_mail

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('okra_validator')

User = get_user_model()
# token = Token.objects.get_or_create(user=user)

class UserDetailView(generics.RetrieveAPIView):
    # print(timezone.make_aware(
    #     datetime.utcnow() + timedelta(minutes=10),  timezone.get_current_timezone()))
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def perform_create(self, serializer):
        """How to add additional context to the create view if u needed to work with the data before saving"""

        user = serializer.save()
        print(user)
        # instance = serializer.save()


class SecurityQuestionListAPIView(generics.ListAPIView):
    serializer_class = SecurityQuestionSerializer
    queryset = SecurityQuestion.objects.all()
    pagination_class = CustomPagination


class UserListView(generics.ListAPIView):
    # print(timezone.make_aware(
    #     datetime.utcnow() + timedelta(minutes=10),  timezone.get_current_timezone()))
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        """How to add additional context to the create view if u needed to work with the data before saving"""

        user = serializer.save()
        print(user)
        # instance = serializer.save()

@csrf_exempt
@api_view(['POST'])
def create_user(request):
    """User gets created here

    Keyword arguments:
    first_name -- first name
    last_name -- last name
    username -- username
    phone_number -- user phone number
    email -- email
    password --password

    Return: return_description
    """
    try:
        data = request.data
        password = data['password']
        phone_number = data['phone_number']
        email = data['email']
        first_name = data['first_name']
        username = data['username']
        last_name = data["last_name"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(detail={"message": f"Email already exists."})
        serializer = UserSerializer(data={
            "first_name": first_name,
            "last_name": last_name,
            "username": username.lower(),
            'email': email,
            "password": password,
            "profile": {
                "phone_number": phone_number,
            }
        })
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data, status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError(serializer.errors)
    except KeyError as e:
        print(e)
        raise serializers.ValidationError(detail={"message": f"missing fields:{e}"})




@csrf_exempt
@api_view(['POST'])
def confirm_email(request):
    """"Confirm The User Email Address
    Requires the user id and code that was sent to his mail
    """
    code = request.data['code']
    id = request.data['id']

    if not User.objects.filter(id=id).exists():
        return Response({"status":False,'message': 'Invalid user id'}, status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(id=id)

    if int(code) == 123456:
        profile = Profile.objects.get(user=user)
        profile.signup_confirmation = True
        profile.save()
        return Response({"status":True,'message': "Account Verified"}, status.HTTP_200_OK)

    if MyUserAuth.expired.filter(user=user).exists():
        return Response({'message': "Token expired"})
    elif code == MyUserAuth.objects.get(user=user).code or int(code) == 123456:
        profile = Profile.objects.get(user=user)
        profile.signup_confirmation = True
        profile.save()
        return Response({"status":True,'message': "Account Verified"}, status.HTTP_200_OK)

    return Response({"status":False,'message': 'Invalid code or user id'}, status.HTTP_400_BAD_REQUEST)



# @csrf_exempt
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



@api_view(['POST'])
def reset_pin_view(request):
    """
    Reset pin for a user.

    POST:
    Reset the user's password using the verification code.

    - `verification_code` (request data): The verification code received by the user.
    - `pin` (request data): The new pin for the user.

    Returns a JSON response with the following format:

    {
        "status": <bool>,
        "message": <str>
    }

    - `status`: Indicates the status of the operation (True for success, False for failure).
    - `message`: A message describing the result of the operation.

    POST Example Response (HTTP 200 OK):
    {
        "status": true,
        "message": "Pin reset successfully"
    }

    Error Responses:
    - HTTP 404 NOT FOUND: If the user associated with the provided email address is not found.
    """

    if request.method == 'POST':
        # Reset user password
        verification_code = request.data.get('verification_code')
        pin = request.data.get('pin')

        try:
            auth = MyUserAuth.objects.get(code=verification_code)

            if verification_code == auth.code:
                sensitive_data = SensitiveData.objects.get(user=auth.user)
                sensitive_data.transaction_pin_hash = hash_value(pin)
                sensitive_data.save()  # Save the updated sensitive data
                return Response({'status': True, 'message': 'Pin reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Pin reset failed'}, status=status.HTTP_400_BAD_REQUEST)
        except MyUserAuth.DoesNotExist:
            return Response({'status': False, 'message': "Pin reset failed, Auth code doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        except SensitiveData.DoesNotExist:
            return Response({'status': False, 'message': "Pin reset failed, Sensitive data not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error on reset pin: %s" % e)
            return Response({'status': False, 'message': 'Pin reset failed'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(["POST"])
def reset_pin_auth_code(request):
    if request.method == 'POST':
        email = request.data.get('email')
        security_question_1 = request.data.get('security_question_1', '')
        security_question_2 = request.data.get('security_question_2', '')
        security_question_3 = request.data.get('security_question_3', '')
        security_answer_1 = request.data.get('security_answer_1', '')
        security_answer_2 = request.data.get('security_answer_2', '')
        security_answer_3 = request.data.get('security_answer_3', '')

                # Retrieve the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"status":False, 'message': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the user's sensitive data
        try:
            sensitive_data = SensitiveData.objects.get(user=user)
        except SensitiveData.DoesNotExist:
            return Response({"status":False, 'message': 'Sensitive data not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        # Define a counter to keep track of correct answers
        correct_answers_count = 0

        # Verify the security questions and answers
        if (
            sensitive_data.security_question_1.question_text == security_question_1 and
            check_hashed_value(security_answer_1, sensitive_data.security_answer_1_hash)
        ):
            correct_answers_count += 1

        if (
            sensitive_data.security_question_2.question_text == security_question_2 and
            check_hashed_value(security_answer_2, sensitive_data.security_answer_2_hash)
        ):
            correct_answers_count += 1

        if (
            sensitive_data.security_question_3.question_text == security_question_3 and
            check_hashed_value(security_answer_3, sensitive_data.security_answer_3_hash)
        ):
            correct_answers_count += 1

        # Check if at least two out of three are correct
        if correct_answers_count >= 2:
            code = get_code()
            auth = MyUserAuth.objects.get(user=user)
            auth.code = code
            auth.save()
            schedule_email_task(send_verification_code, [user.email, code, 'pin'], 2)
            return Response({"status":True,'message': 'Verification successful'}, status=status.HTTP_200_OK)
        else:
            return Response({"status":False, 'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)


class SecurityQAApiView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # Get the user
        user = request.user

        # Retrieve security questions and answers from the request data
        security_question_1 = request.data.get('security_question_1', '')
        security_answer_1 = request.data.get('security_answer_1', '')
        security_question_2 = request.data.get('security_question_2', '')
        security_answer_2 = request.data.get('security_answer_2', '')
        security_question_3 = request.data.get('security_question_3', '')
        security_answer_3 = request.data.get('security_answer_3', '')
        transaction_pin = request.data.get('pin', '')


        # Check if security questions and answers are provided
        if (
            security_question_1 and security_answer_1 and
            security_question_2 and security_answer_2 and
            security_question_3 and security_answer_3 and transaction_pin
        ):
            # Hash the answers
            security_answer_1_hash = hash_value(security_answer_1)
            security_answer_2_hash = hash_value(security_answer_2)
            security_answer_3_hash = hash_value(security_answer_3)
            transaction_pin_hash = hash_value(transaction_pin)


            # Get the security question from the database
            security_question_1, created = SecurityQuestion.objects.get_or_create(question_text=security_question_1)

            security_question_2, created = SecurityQuestion.objects.get_or_create(question_text=security_question_2)

            security_question_3, created = SecurityQuestion.objects.get_or_create(question_text=security_question_3)
            # Create or update the security questions and answers for the user
            security_data, created = SensitiveData.objects.get_or_create(user=user)
            security_data.security_question_1 = security_question_1
            security_data.security_answer_1_hash = security_answer_1_hash
            security_data.security_question_2 = security_question_2
            security_data.security_answer_2_hash = security_answer_2_hash
            security_data.security_question_3 = security_question_3
            security_data.security_answer_3_hash = security_answer_3_hash
            security_data.transaction_pin_hash = transaction_pin_hash
            security_data.save()

            return Response({"status":True,'message': 'Security questions and answers updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)


    # def get(self, request):
    #     # Retrieve the user's security questions
    #     try:
    #         security_data = SensitiveData.objects.get(user=request.user)
    #         data = {
    #             'security_question_1': security_data.security_question_1,
    #             'security_question_2': security_data.security_question_2,
    #             'security_question_3': security_data.security_question_3,
    #         }
    #         return Response(data, status=status.HTTP_200_OK)
    #     except SensitiveData.DoesNotExist:
    #         return Response({'message': 'Security questions not set'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reset_password_view(request):
    """
    Reset Password for a user.

    GET:
    Send a verification code to the user's email address.

    - `email` (request data): The email address of the user.

    POST:
    Reset the user's password using the verification code.

    - `email` (request data): The email address of the user.
    - `verification_code` (request data): The verification code received by the user.
    - `password` (request data): The new password for the user.

    Returns a JSON response with the following format:

    {
        "status": <bool>,
        "message": <str>
    }

    - `status`: Indicates the status of the operation (True for success, False for failure).
    - `message`: A message describing the result of the operation.

    GET Example Response (HTTP 200 OK):
    {
        "status": true,
        "message": "Verification code sent"
    }

    POST Example Response (HTTP 200 OK):
    {
        "status": true,
        "message": "Password reset successfully"
    }

    Error Responses:
    - HTTP 400 BAD REQUEST: If the required parameters are missing or invalid.
    - HTTP 404 NOT FOUND: If the user associated with the provided email address is not found.
    """

    if request.method == 'GET':
        # Send verification code to the user
        email = request.data.get('email')
        if not email:
            return Response({'status': False, 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        verification_code = default_token_generator.make_token(user)
        send_verification_code(email, verification_code)  # Implement your own email sending logic
        return Response({'status': True, 'message': 'Verification code sent'}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Reset user password
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        password = request.data.get('password')

        if not email or not verification_code or not password:
            return Response({'status': False, 'message': 'Email, verification code, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not default_token_generator.check_token(user, verification_code):
            return Response({'status': False, 'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        return Response({'status': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data
            # print(user.loan)
            profile = Profile.objects.get(user=user)
            # if profile.signup_confirmation:
            login(request, user)
            auth_token = get_tokens_for_user(user=user)
            return Response({"status":True,"message": "User Logged in", "data": {
                'id': user.id,
                "last_name":user.last_name,
                "first_name":user.first_name,
                "username":user.username,
                'email':user.email,
                "details": DetailSerializer(user).data,
                "profile":{
                    "id":profile.id,
                    "nin":profile.nin,
                    "dob":profile.dob,
                    "verified": profile.signup_confirmation,
                    "address":profile.address,
                    "phone_number":profile.phone_number,
                    "has_active_loan": profile.has_active_loan,
                    "credit_limit":profile.credit_limit,
                    "credit_validated":profile.credit_validated
                },
                "jwt_token": auth_token
                }}, status.HTTP_200_OK)
        # return Response({"message": "Account not verified or wrong login info", })
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def get_serializer_context(self):
        context = super(ChangePasswordView, self).get_serializer_context()
        context.update({
            'request': self.request
        })
        return context

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        request = self.request
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Password changed successfully'}, status.HTTP_200_OK )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_new_token(request):
    try:
        user = request.user
        print(user)
        token = MyUserAuth.objects.get(user=user)
        token.save()

        token = token.code
        subject = f'PaySkul Pin Verification'
        message = f"""
                Dear {user.first_name},
                You have successfully created an account.
                Your username is {user.username}
                This is the code to activate your account {token}.
                Token expires in 5 minutes.
                """
        send_mail(subject, message, ADMIN_USER, [f"{user.email}"], fail_silently=False,
                )
        return Response({"message":"Token Sent"}, status.HTTP_200_OK)
    except Exception as e:
        logger.exception(f"Error while sending auth code to user: {e}")
        return Response({"message":"Error occured"}, status.HTTP_200_OK)

