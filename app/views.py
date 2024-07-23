from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['label', 'balance']
    ordering_fields = ['label', 'balance']
    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['wallet', 'txid', 'amount']
    ordering_fields = ['txid', 'amount']
