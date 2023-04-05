from rest_framework import serializers
from . models import *

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Category
        fields = ('id', 'name', 'slug')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'slug', 'deposit_rate', 'description')


class TransactionSerializer(serializers.ModelSerializer):
    
    total_payments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'date', 'amount', 'description', 'type', 'loan', 'total_payments')
        
    def get_total_payments(self, obj):
        return obj.get_total_payments()


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
        fields = ('id', 'user', 'name', 'number', 'cvv')