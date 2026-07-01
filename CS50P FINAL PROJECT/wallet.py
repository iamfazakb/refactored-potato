import csv
import datetime
import requests

#Constants for the program.
CSV_FILE = "transactions.csv"
EXCHANGE_FEE_PERCENT = 1.5  
API_KEY = "4dae06a49fefbbadd8fbae34"  #Created by Alex
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest"

class Wallet:
    """Wallet class for managing currency and expenses."""

    def __init__(self, currency: str, currency_amount: float) -> None:
        '''Initializes a new Wallet(Dictionary), taking in currency as a STR and currency_amount as a FLOAT.'''
        
        self.accounts: dict[str, float] = {currency.upper(): currency_amount} #.upper() introduced so it automatically uppercases the currency, i.e "usd" to "USD"
        
    def __str__(self):
        '''Prints current balance inside the Wallet.'''
        
        output = ""  
        for key, value in self.accounts.items():
            output += f"{key}: {value:.2f}\n"   
        return output.strip()

        #Key changes:
        # Since the dictionary has multiple currencies' amounts at the same time, 
        # we cannot just return the first item in the dictionary. 
        # this code iterates over the dictionary, adds the items to a new string and 
        # in the end returns that string.

        # STATUS: tested. 

    def exchange_currency(self, currency: str, target_currency: str, currency_amount: float) -> None:
        '''Exchanges currency to the user's desired one. Error-Handling has been put in place to prevent malicious attempts.'''

        currency, target_currency = currency.upper(), target_currency.upper()
        #Uppercases the currency to prevent "usd" vs "USD"

        '''Error Handling'''
        if currency not in self.accounts:
            raise ValueError(f"You don't possess an active account in {currency}")
        elif currency_amount <= 0 or currency_amount > self.accounts[currency]:
            raise ValueError(f"Invalid amount or insufficient funds for exchange.")
        

        '''Contacts server for the live exchange rates.'''
        url = f"{API_URL}/{currency}"
        data = self._request_rates(url)

        '''Checks the dataset for invalid structure or invalid target currency.'''
        if not data or 'conversion_rates' not in data:
            raise ConnectionError("Error: Invalid Data Structure Received")
        elif target_currency not in data['conversion_rates']:
            raise ValueError(f"Error: {target_currency} is invalid or unsupported.")
        
            

        '''Initializes the rate, by extracting it from nested dictionary'''
        rate = data['conversion_rates'][target_currency]



        '''Converts the currency to the desired one, while subtracting the exchange fee.'''
        charge = currency_amount * (EXCHANGE_FEE_PERCENT/100)
        spendable_amount = currency_amount - charge
        exchanged_amount = spendable_amount*rate
        


        '''Update the amounts in the dictionary'''
        self.accounts[currency] -= currency_amount
        self.accounts[target_currency] = self.accounts.get(target_currency, 0.0) + exchanged_amount
 
        '''Log and print the transaction details to the user.'''
        exchange_detail: str = f'Exchanged {currency}: {currency_amount} to {target_currency}: {exchanged_amount} (Fee: {charge:.2f} {currency})'
        self._write_transaction(currency_amount, exchange_detail)
        print(exchange_detail)

        #Key changes: 
        #used less code compared to before
        # logic remains the same, variables renamed for convenience

        #STATUS: TESTED

    def _request_rates(self, url: str) -> dict:
        """A recursive helper function that returns a response object
        in json format from the exchange rates API.
        """
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException:
            print("Unable to fetch exchange rates from server. Try Again")
            return {}

    def spend_currency(self, currency: str, amount: float) -> None:
        '''Deducts funds from a currency amount to track spending.'''
        currency = currency.upper()

        '''Error Handling'''
        if currency not in self.accounts or amount > self.accounts[currency]:
            raise ValueError("Insufficient funds or no active account from the selected currency.")
        elif amount <= 0:
            raise ValueError("Invalid argument. Try again")
        
        '''Subtracts funds, logs the transaction.'''
        self.accounts[currency] -= amount
        self._write_transaction(amount, f"Spent local funds in {currency}")
        print(f"Success! Spent {amount:.2f}{currency}")
        ...

    def print_receipt(self):  
        '''Generates a PDF file, containing all the transactions and final wallet balance.'''

        #To be worked on.
        ...

    def _write_transaction(self, amount: float, detail: str) -> None:
        """A helper function to open and write to a csv file."""

        fieldnames = ['time', 'amount', 'detail']
        with open('transactions.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'amount': amount,
                'detail': detail,
                })

    def expenses(self) -> None:
        """A helper function to open and read a csv file cleanly."""
        
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"\n{'TIMESTAMP':<21} | {'AMOUNT':<10} | {'TRANSACTION DESCRIPTION'}")
            print("-" * 70)
            # 4. Loop over every row inside the CSV file and align the data fields
            for row in reader:
                print(f"{row['time']:<21} | {row['amount']:<10} | {row['detail']}")
   

