from rest_framework import serializers

# from account.serializers import ProfileInlineSerializer
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
    loan = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=100, decimal_places=2)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'user', 'amount')


class WalletInlineSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(read_only=True, max_digits=100, decimal_places=2)


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ('id', 'user', 'service', 'start_date', 'end_date', "amount_to_pay_back",'total_repayment', 'cleared')


class LoanInlineSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)
    amount_needed = serializers.DecimalField(read_only=True, max_digits=100, decimal_places=2)
    amount_to_pay_back = serializers.DecimalField(read_only=True, max_digits=100, decimal_places=2)
    cleared = serializers.BooleanField(read_only=True)


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'user', 'name', 'balance')


class CardSeriilizer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "user", "number", "name",  "cvv")
        
      
class CardInlineSerializer(serializers.Serializer)  :
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.CharField(read_only=True)
    number = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    


class DetailSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    transactions = TransactionInlineSerializer()
    loan = LoanInlineSerializer()
    card = CardInlineSerializer()
    class Meta:
        model = User
        fields = ("id", "username", "email", "wallet", "transactions", "loan", "card")
    
    def get_transactions(self, obj):
        return TransactionInlineSerializer(obj.transactions, context=self.context).data
    
    def get_loan(self, obj):
        return LoanInlineSerializer(obj.loan, context=self.context).data
    
    def get_card(self, obj):
        return CardInlineSerializer(obj.card, context=self.context).data
    
    def get_wallet(self, obj):
        return WalletInlineSerializer(obj.wallet, context=self.context).data
