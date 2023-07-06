from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.timezone import now
from hashid_field import Hashid
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.tasks import send_auth_mail
from .utils import verify_email_smtp
from .models import Profile, UserAuthCodes
from payskul.settings import ADMIN_USER
from payskul.settings import EMAIL_HOST_USER as admin_mail
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password

User = get_user_model()




class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'address', 'nin']
        read_only_fields = ('signup_confirmation',)


class ProfileInlineSerializer(serializers.Serializer):
    nin = serializers.CharField(read_only=True)
    dob = serializers.DateTimeField(read_only=True)
    address = serializers.CharField(read_only=True)


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
            user.set_password(validated_data['password'])
            user.save()
            profile_data["user"] = user
            Profile.objects.create(**profile_data)
            try:
                token = UserAuthCodes.objects.get(user=user).code
                subject = f"PaySkul Password Reset Pin"
                message = f"""
                Dear {user.first_name},
                You have successfully created an account.
                Your username is {user.username}
                This is the code to activate your account {token}.
                """
                send_mail(subject=subject,
                                    message=message,
                                    from_email=admin_mail,
                                    recipient_list=[user.email],
                                    fail_silently=False
                                    )
                return user
            except  Exception as e:
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
        
    # def get_token(self, obj):
    #     print(obj)
    #     return Token.objects.get(user=obj).key
    
    # def get_referrals(self, obj):
    #     print(obj.id)
    #     return Profile.objects.get(user=obj).get_recommened_profiles() if Profile.objects.filter(user=obj).exists() else "No referrals"
        

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # email = serializers.CharField(read_only=True)
    # profile = serializers.SerializerMethodField(read_only=True)
    
    # class Meta:
    #     model = User
        
    def validate(self, data):
        print(data)
        user = authenticate(**data)
        if user and user.is_active:
            return user
        print(user)
        raise serializers.ValidationError({
            "status": False,
            "message": "Username and or password incorrect."
        }, code="400")
        # return data
    
    # def get_profile(self, obj):
    #     return ProfileInlineSerializer(obj.profile, context=self.context).data
    
    
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
