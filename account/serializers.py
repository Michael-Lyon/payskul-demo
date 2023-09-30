from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.timezone import now
from hashid_field import Hashid
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.tasks import send_auth_mail
from scheduled_tasks.my_tasks import schedule_email_task
from .utils import get_code, send_signup_email, verify_email_smtp
from .models import Profile, MyUserAuth, SecurityQuestion
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password

User = get_user_model()




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'address']
        read_only_fields = ('signup_confirmation',)


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityQuestion
        fields = ['id', 'question_text']

class ProfileInlineSerializer(serializers.Serializer):
    nin = serializers.CharField(read_only=True)
    dob = serializers.DateTimeField(read_only=True)
    address = serializers.CharField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    # referrals = serializers.SerializerMethodField()
    # token = serializers.SerializerMethodField(read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id','first_name', 'username', 'last_name', 'password', 'email',  'profile']

    def create(self, validated_data):
        # create user
        # print(validated_data)
        profile_data = validated_data.pop('profile')
        try:
            user = User.objects.create_user(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            profile_data["user"] = user
            profile = Profile.objects.create(**profile_data)
            profile.ref_code = user.username
            profile.save()
            code = get_code()
            auth = MyUserAuth.objects.get_or_create(user=user)
            auth.code = code
            auth.save()
            try:
                schedule_email_task(send_signup_email, email_function_args=[user, code], delay_seconds=1)
                return user
            except  Exception as e:
                print(e)
                user.delete()
                raise serializers.ValidationError(
                {
                    "status": False,
                    "message": "Something went wrong. Please try again."
                }, code="400"
                    )

        except Exception as e:
            print(e)
            user.delete()
            raise serializers.ValidationError(
                {
            "status": False,
            "message": "Something went wrong. Please try again."
            }, code="400"
                )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({
                'detail': 'Unable to log in with provided credentials.',
                'username': 'Check your username.',
                'password': 'Check your password.',
            }, code="authentication_failed")


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.context.get('request', None)
        return context


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError({"message": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
