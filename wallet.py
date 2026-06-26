import requests

class Wallet:
    """Wallet class for managing currency and expenses."""

    def __init__(self, code_base: str, currency_ammount: float):
        """Intialize variables to store class states."""

        # I'd prefer it more if the dictionary is used instead.
        # Every piece of data should have only one representation.
        # self.code_base = code_base
        # self.currency_ammount = currency_ammount

        # A dictionary to keep track of currencies the user has.
        self.accounts: dict[str: float] = {code_base: currency_ammount}

    def print_currency(self):
        for key, value in self.accounts.items():
            print(key, value)

    def exchange_currency(self, code_base: str, code_target: str, currency_ammount: float):
        """TODO: Yeah, I forgot how to do proper docstrings.
        Well, for now just know that this method exchanges currency
        into other country currencies.
        """
        if currency_ammount < 0\
            or currency_ammount > self.accounts[code_base]:
            raise Exception

        # Try to check if the user has the base currency,
        # the user's trying to exchange.
        if not self.accounts.get(code_base):
            raise Exception

        # TODO: Catch errors raised by these lines.
        # Rates By Exchange Rate API, https://www.exchangerate-api.com.
        url = f'https://open.er-api.com/v6/latest/{code_base}'
        response = requests.get(url)
        data = response.json()

        # I need to find a way to do this using if statements.
        try: rate: float = data['rates'][code_target]
        except KeyError: raise Exception

        self.accounts[code_base] -= currency_ammount
        exchanged_ammount: float = currency_ammount * rate
        # Add the exchanged currency to the accounts dictionary
        self.accounts[code_target] = exchanged_ammount

        print(f'Exchanged {code_base}: {currency_ammount} to {code_target}: {exchanged_ammount}')

    def spend_currency(self, code, amount):
        ...

    def print_expenses(self):
        ...

    def print_receipt(self):
        ...


if __name__ == '__main__':
    wallet = Wallet('USD', 100)