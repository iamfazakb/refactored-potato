from wallet import Wallet 

def main():
    while True:
        try:
            creation = input("Currency and Funds (seperate by a comma): ")
            currency, funds = creation.strip().split(",")
            funds = float(funds)
            break
        except ValueError:
            print("Invalid args. Try Again")
            continue
    
    wallet = Wallet(currency, funds)
    prompt = "\n---- Real-Time Currency and Expense Tracker ----\n \nSelect an option(1-4)\n 1. Convert currency and spend money\n 2. View your past trip expenses\n 3. Export an official trip receipt document\n 4. Exit the app.\n"
    opt = int(input(prompt))

'''IN PROGRESS'''

# def wallet_testing():
#     #creating this function to understand the Wallet class and testing it for new changes.
    
#     wallet = Wallet("USD", 500.00)
#     print(wallet)
#     wallet.exchange_currency("USD", "INR", 500.00)

# wallet_testing()

if __name__ == "__main__":
    main()