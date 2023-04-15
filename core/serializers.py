from rest_framework import serializers

from account.serializers import ProfileInlineSerializer
from . models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Category
        fields = ('id', 'name', 'slug')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id',"service_category" ,'name', 'slug', 'deposit_rate', 'description')


class TransactionSerializer(serializers.ModelSerializer):
    
    my_total_payments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'date', 'amount', 'description', 'type', 'loan', 'my_total_payments')
        
    def get_my_total_payments(self, obj):
        if not hasattr(obj, 'id'):
            return None
        else:
            return obj.get_total_payments()


class TransactionInlineSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=100, decimal_places=2)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'user', 'amount')


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'user', 'service', 'down_payment', 'amount_needed',
                  'start_date', 'end_date', 'total_repayment', 'cleared')


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'user', 'name', 'balance')


class CardSeriilizer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "number", "name", 'user', "cvv")
        
        



class DetailSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    transactions = TransactionSerializer()
    profile = ProfileInlineSerializer(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile", "wallet", "transactions", )
    
    def get_profile(self, obj):
        return ProfileInlineSerializer(obj.profile, context=self.context).data
