from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.timezone import now
from hashid_field import Hashid
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.tasks import send_auth_mail
from .models import Profile, UserAuthCodes
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail
from django.core.mail import send_mail

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'address', 'nin']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    # referrals = serializers.SerializerMethodField()
    # token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id','first_name', 'username', 'last_name', 'password', 'email',  'profile']
        
    def create(self, validated_data):
        # create user 
        # print(validated_data)
        profile_data = validated_data.pop('profile')
        try:
            user = User.objects.create_user(**validated_data)
            profile_data["user"] = user
            Profile.objects.create(**profile_data)
            return user
        except Exception as e:
            print(e)
            user.delete()
            raise serializers.ValidationError("Something went wrong please try again")
        
    # def get_token(self, obj):
    #     print(obj)
    #     return Token.objects.get(user=obj).key
    
    # def get_referrals(self, obj):
    #     print(obj.id)
    #     return Profile.objects.get(user=obj).get_recommened_profiles() if Profile.objects.filter(user=obj).exists() else "No referrals"
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
    