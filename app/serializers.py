# payments/serializers.py

from rest_framework import serializers
from django.db import transaction as db_transaction
from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Wallet
        fields = '__all__'

    def validate(self, data):
        # Validate that balance is not negative
        if data['balance'] < 0:
            raise serializers.ValidationError("Balance cannot be negative")
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        with db_transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(
                id=validated_data['wallet'].id
            )
            new_balance = wallet.balance + validated_data['amount']
            if new_balance < 0:
                raise serializers.ValidationError(
                    "Resulting balance cannot be negative"
                )

            transaction = Transaction.objects.create(**validated_data)
            wallet.balance = new_balance
            wallet.save()
        return transaction
