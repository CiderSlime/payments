import pytest
from rest_framework.test import APIClient
from app.models import Wallet, Transaction
import threading


@pytest.mark.django_db
def test_transaction_creation_updates_wallet_balance():
    client = APIClient()
    wallet = Wallet.objects.create(label='Test Wallet', balance=0)

    data = {'wallet': wallet.id, 'txid': 'tx123', 'amount': 50}
    response = client.post('/api/transactions/', data, format='json')
    assert response.status_code == 201
    wallet.refresh_from_db()
    assert wallet.balance == 50

    data = {'wallet': wallet.id, 'txid': 'tx124', 'amount': -20}
    response = client.post('/api/transactions/', data, format='json')
    assert response.status_code == 201
    wallet.refresh_from_db()
    assert wallet.balance == 30

    data = {'wallet': wallet.id, 'txid': 'tx125', 'amount': -50}
    response = client.post('/api/transactions/', data, format='json')
    assert response.status_code == 400
    wallet.refresh_from_db()
    assert wallet.balance == 30


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    'initial_balance,expected_balance,transaction_count',
    [
        (100, 40, 1),  # balance sufficient for only one transaction
        (120, 0, 2)    # enough balance for both transactions
    ]
)
def test_concurrent_transactions(
    initial_balance, expected_balance, transaction_count
):
    """Test that only"""
    client = APIClient()
    wallet = Wallet.objects.create(
        label='Concurrent Wallet', balance=initial_balance
    )

    data1 = {
        'wallet': wallet.id,
        'txid': 'tx_concurrent_1',
        'amount': -60
    }
    data2 = {
        'wallet': wallet.id,
        'txid': 'tx_concurrent_2',
        'amount': -60
    }

    def create_transaction(data):
        response = client.post('/api/transactions/', data, format='json')
        return response

    thread1 = threading.Thread(target=create_transaction, args=(data1,))
    thread2 = threading.Thread(target=create_transaction, args=(data2,))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert Transaction.objects.count() == transaction_count
    expected_balance = expected_balance

    wallet.refresh_from_db()
    assert wallet.balance == expected_balance
