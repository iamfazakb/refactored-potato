import pytest
import requests
from wallet import Wallet


def test_exchange_currency():
    # I forgot how to setup environments for testing.
    wallet = Wallet('USD', 1)
    wallet.exchange_currency('USD', 'AUD', 1)
    # How would it be possible to check exchange rates I wonder?
    wallet.accounts['AUD'] = requests.get('https://open.er-api.com/v6/latest/AUD').json()['rates']['AUD']
    # Check for currency subtraction after exchange.
    wallet.accounts['USD'] = 0


def test_exchange_currency_raises():
    # Are these useful? I mean the user will never see these methods.
    # In a way these checks are only for us.
    with pytest.raises(Exception):
        # Check for proper base code.
        wallet.exchange_currency('US', 'AUD', 1)
    with pytest.raises(Exception):
        # Check for proper target code.
        wallet.exchange_currency('USD', 'AU', 1)
    with pytest.raises(Exception):
        # Check for proper currency ammount.
        wallet.exchange_currency('USD', 'AUD', -1)
    with pytest.raises(Exception):
        wallet = Wallet('USD', 0)
        # Check for proper currency ammount.
        wallet.exchange_currency('USD', 'AUD', 1)