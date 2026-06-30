import csv
import datetime
import requests

class Wallet:
    """Wallet class for managing currency and expenses."""

    def __init__(self, code_base: str, currency_ammount: float) -> None:
        """Intialize variables to store class states."""

        # I'd prefer it more if the dictionary is used instead.
        # Every piece of data should have only one representation.
        # self.code_base = code_base
        # self.currency_ammount = currency_ammount

        # A dictionary to keep track of currencies the user has.
        self.accounts: dict[str: float] = {code_base: currency_ammount}

    def print_currency(self) -> None:
        for key, value in self.accounts.items():
            print(key, value)

    def exchange_currency(self, code_base: str, code_target: str, currency_ammount: float) -> None:
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

        # Rates By Exchange Rate API, https://www.exchangerate-api.com.
        url = f'https://open.er-api.com/v6/latest/{code_base}'
        data = self._request_rates(url)

        # I need to find a way to do this using if statements.
        try: rate: float = data['rates'][code_target]
        except KeyError: raise Exception

        self.accounts[code_base] -= currency_ammount
        exchanged_ammount: float = currency_ammount * rate
        # Add the exchanged currency to the accounts dictionary
        self.accounts[code_target] = exchanged_ammount

        exchange_detail: str = f'Exchanged {code_base}: {currency_ammount} to {code_target}: {exchanged_ammount}'
        self._write_transaction(currency_ammount, exchange_detail)
        print(exchange_detail)

    def spend_currency(self, code, amount):
        ...

    def print_expenses(self):
        """Not going to write a docstring for this function just yet."""
        self._read_transaction()

    def print_receipt(self):
        ...

    def _write_transaction(self, amount: float, detail: str) -> None:
        """A helper function to open and write to a csv file."""
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ['time', 'amount', 'detail']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'time': datetime.datetime.now(),
                'amount': amount,
                'detail': detail,
                })

    def _read_transaction(self):
        """A helper function to open and read a csv file."""
        with open('transactions.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row['time'], row['amount'], row['detail'])

    def _request_rates(self, url: str) -> dict:
        """A recursive helper function that returns a response object
        in json format from the exchange rates API.
        """

        # Maybe I should not do this. You live and learn I guess.
        try:
            response: requests.Response = requests.get(url)
            return response.json()
        except requests.exceptions:
            self._request_rates(url)



if __name__ == '__main__':
    wallet = Wallet('USD', 100)
    wallet.print_expenses()