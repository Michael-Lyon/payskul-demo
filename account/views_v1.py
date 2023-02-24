from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, login
from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from account.models import Profile, UserAuthCodes
from account.serializers import LoginSerializer, ProfileSerializer, UserSerializer
from account.utils import get_code

from payskul.settings import EMAIL_HOST_USER as admin_mail

User = get_user_model()
# token = Token.objects.get_or_create(user=user)


class UserListView(generics.ListAPIView):
    # print(timezone.make_aware(
    #     datetime.utcnow() + timedelta(minutes=10),  timezone.get_current_timezone()))
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def perform_create(self, serializer):
    #     """How to add additional context to the create view if u needed to work with the data before saving"""
    #     # instance = serializer.save()
    # if isinstance(instance, User):


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

        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            # TODO: REMOVE THIS PART PNCE SMTP IS SETUP PROPERLY
            data['verification-code'] = UserAuthCodes.objects.get(id=data['id']).code
            return Response(data)
        else:
            raise serializers.ValidationError(serializer.errors)
    else:
        raise serializers.ValidationError("Invalid signup data.")


@api_view(['POST'])
def confirm_email(request):
    """"Confirm The User Email Address
    Requires the user id and code that was sent to his mail
    """
    code = request.data['code']
    id = request.data['id']
    user = User.objects.get(id=id)
    if UserAuthCodes.expired.filter(user=user).exists():
        print(timezone.now())
        print("===================")
        print(UserAuthCodes.objects.get(user=user).expires_at)
        return Response({'message': "Token expired"})
    elif code == UserAuthCodes.objects.get(user=user).code:
        profile = Profile.objects.get(user=user)
        profile.signup_confirmation = True
        profile.save()
        return Response({'message': "Account Verified"})
    return Response({'message': 'Invalid code or user id'}, status=404)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if Profile.objects.get(user=user).signup_confirmation:
                login(request, user)
                return Response({"message": "User Logged in", "data": {
                    'id': user.id,
                }})
            return Response({"message": "Account not verified or wrong login info", })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
