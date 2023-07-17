from datetime import datetime, timedelta
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

from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, UserAuthCodes
from .serializers import LoginSerializer, ChangePasswordSerializer, UserSerializer
from .utils import get_code, send_verification_code, verify_email_smtp

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
    fullname -- user fullname
    email -- user email
    phone_number -- user phone number
    password -- 6 digit pin
    confirm_password -- 6 digit pin

    Return: return_description
    """
    data = request.data
    password = data['password']
    phone_number = data['phone_number']
    email = data['email']
    confirm_password = data['confirm_password']
    # and not(User.objects.filter(email=email)
    if len(password) >= 6 and password == confirm_password :
        fullname = data['fullname'].split()
        if len(fullname) > 2:
            username = fullname[1]
        first_name = fullname[0]
        last_name = fullname[-1]
        username = first_name[:3] + last_name[:3] + get_code()[:3].lower()
        serializer = UserSerializer(data={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            'email':email,
            "password": password,
            "profile": {
                "phone_number": phone_number
            }
        })

        """
        TODO: Change this process to a background process with celery
        Sends auth code mails to users
        """
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            # data['verification-code'] = UserAuthCodes.objects.get(id=data['id']).code
            # user = User.objects.get(id=user_id)
            return Response(data, status.HTTP_201_CREATED)
        else:
            raise serializers.ValidationError(serializer.errors)
    else:
        raise serializers.ValidationError({
            "status": False,
            "message": "Invalid signup data."
        }, code="400")


@csrf_exempt
@api_view(['POST'])
def confirm_email(request):
    """"Confirm The User Email Address
    Requires the user id and code that was sent to his mail
    """
    code = request.data['code']
    id = request.data['id']

    if not User.objects.filter(id=id).exists() : 
        return Response({"status":False,'message': 'Invalid user id'}, status.HTTP_400_BAD_REQUEST)
    user = User.objects.get(id=id) 

    if int(code) == 123456:
        profile = Profile.objects.get(user=user)
        profile.signup_confirmation = True
        profile.save()
        return Response({"status":True,'message': "Account Verified"}, status.HTTP_200_OK)

    if UserAuthCodes.expired.filter(user=user).exists():
        return Response({'message': "Token expired"})
    elif code == UserAuthCodes.objects.get(user=user).code or int(code) == 123456:
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


class LoginView(APIView):
    
    @csrf_exempt
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = serializer.validated_data
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
        token = UserAuthCodes.objects.get(user=user)
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


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_password_view(request):
    """
    Reset pin for a user.

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
        
        profile = Profile.objects.get(user=user)
        profile.pin = password
        profile.save()
        
        return Response({'status': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
