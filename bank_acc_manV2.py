import datetime
import os
import re


def main_menu():
    print("************************************************************")
    print("                  Dobrodošli u PyBANK ALGEBRA               ")
    print("************************************************************")
    print("| 1. Kreiranje računa                                      |")
    print("| 2. Prikaz stanja računa                                  |")
    print("| 3. Prikaz prometa po računu                              |")
    print("| 4. Polog novca na račun                                  |")
    print("| 5. Oročenje sa kamatom od 2% godišnje                    |")
    print("| 6. Podizanje novca s računa                              |")
    print("| 7. Izlaz iz programa                                     |")
    print("************************************************************")




def check_oib(oib):
    return bool(re.match(r'^\d{11}$', oib))



def generate_account_number(account_number):
    year, month = datetime.datetime.now().year, datetime.datetime.now().month
    month_str = f"{month:02d}"

    if not account_number:
        account_number = f"BA-{year}-{month_str}-00001"
    else:
        number = int(account_number.split('-')[-1]) + 1
        account_number = f"BA-{year}-{month_str}-{str(number).zfill(5)}"

    return account_number



def open_account(accounts):
    account_number = None
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"KREIRANJE RACUNA".center(65)}\n\n{"Podaci o vlasniku racuna".center(65)}\n\n')

    name = input("Unesite naziv firme: ")
    address = input("Unesite adresu firme: ")
    oib = input("Unesite OIB firme: ")
    
    while not check_oib(oib):
        print("OIB mora imati 11 brojki.")
        oib = input("Unesite OIB firme: ")
        
    responsible_person = input("Unesite ime odgovorne osobe: ")
    currency = '€'

    account_number = generate_account_number(account_number)

    accounts[account_number] = {
        'name': name,
        'address': address,
        'oib': oib,
        'responsible_person': responsible_person,
        'balance': 0,
        'transactions': []
    }

    input('\nSPREMI? (Stisnite bilo koju tipku) ')

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"KREIRANJE RACUNA".center(65)}\n\n')
    print(f'Podaci o vlasniku racuna tvrtke {name}, su uspjesno spremljeni.')
    input('Za nastavak pritisnite bilo koju tipku\t')

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"KREIRANJE RACUNA".center(65)}\n\n{"Stanje racuna".center(65)}\n\n')

    print(f'Broj racuna {account_number}')
    deposit_amount = input('Unesite iznos za uplatu: ')
    
    while True:
        try:
            deposit_amount = float(deposit_amount)
            if deposit_amount <= 0:
                print("Iznos mora biti veći od nule.")
                deposit_amount = input('Unesite iznos za uplatu: ')
            else:
                break
        except ValueError: 
            print("Molimo unesite validan iznos.")
            deposit_amount = input('Unesite iznos za uplatu: ')

    accounts[account_number]['balance'] += deposit_amount
    transaction = {'date': datetime.datetime.now().date().strftime("%d.%m.%Y"),
                   'time': datetime.datetime.now().time().strftime("%H:%M"),
                   'amount': deposit_amount,
                   'description': "Polog: " + str(deposit_amount) + " EUR"}
    accounts[account_number]['transactions'].append(transaction)

    print(f'Uplata od {deposit_amount:.2f}{currency} je uspješno unešena. Novo stanje računa je {accounts[account_number]["balance"]:.2f}{currency}.')



def display_balance(accounts):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"PREGLED STANJA RACUNA".center(65)}\n\n{"*******************".center(65)}\n\n')
    account_number = input("Unesite broj računa: ")
    if account_number in accounts:
        print(f"Stanje na računu: {accounts[account_number]['balance']:.2f} EUR")
    else:
        print("Račun nije pronađen.")



def display_transactions(accounts):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"PREGLED TRANSAKCIJA RACUNA".center(65)}\n\n{"ISPIS TRANSAKCIJA".center(65)}\n\n')

    account_number = input("Unesite broj računa: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Ispis transkacija za racun {account_number}:')
    if account_number in accounts:
        print(f"{'ID':<5} | {'Datum':<10} | {'Vrijeme':<8} | {'Iznos':<10}  | {'Broj Računa':^15}  | Opis plaćanja")
        
        for i, transaction in enumerate(accounts[account_number]['transactions']):
            transaction_id = i + 1
            date = transaction['date']
            time = transaction['time']
            amount = '{:.2f}'.format(transaction['amount']) + " EUR"
            description = transaction['description']
            
            print(f"{transaction_id:<5} | {date:^10} | {time:^8} | {amount:>11} | {account_number:^17}| {description}")
            
    else:
        print("Račun nije pronađen.")



def deposit(accounts):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"UPLATA NA RACUN".center(65)}\n\n{"DEPOZIT".center(65)}\n\n')

    account_number = input("Unesite broj računa: ")

    try:
        amount = float(input("Unesite iznos za uplatu: "))
    except ValueError:
        print("Neispravan iznos.")
        return

    if account_number in accounts:
        accounts[account_number]['balance'] += amount
        transaction = {'date': datetime.datetime.now().date().strftime("%d.%m.%Y"),
                       'time': datetime.datetime.now().time().strftime("%H:%M"),
                       'amount': amount,
                        'description': "Uplata: {:.2f} EUR".format(amount)
                        }
        accounts[account_number]['transactions'].append(transaction)
        print("Novac uspješno uplaćen.")
    else:
        print("Račun nije pronađen.")


def time_deposit(accounts):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"OROČENA ŠTEDNJA".center(65)}\n\n{"FIKSNA KAMATA OD 2%".center(65)}\n\n')
    account_number = input("Unesite broj računa: ")
    try:
        deposit_amount = float(input("Unesite iznos za oročenje: "))
        years = int(input("Unesite broj godina za oročenje: "))
    except ValueError:
        print("Neispravan unos.")
        return

    if account_number in accounts:
        if deposit_amount <= accounts[account_number]['balance']:
            accounts[account_number]['balance'] -= deposit_amount   # subtract the deposit amount from the balance
            interest = deposit_amount * (1 + 0.02) ** years
            transaction = {
                'date': datetime.datetime.now().date().strftime("%d.%m.%Y"),
                'time': datetime.datetime.now().time().strftime("%H:%M"),
                'amount': interest,
                'description': "Orocenje:  {:.2f} EUR".format(interest)
            }
            accounts[account_number]['transactions'].append(transaction)
            print(f"Oročenje uspješno. Ukupna kamata: {interest:.2f} EUR")
        else:
            print("Nemate dovoljno sredstava na računu.")
    else:
        print("Račun nije pronađen.")




def withdraw(accounts):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{"*" * 65}\n{"PyBANK ALGEBRA".center(65)}\n\n')
    print(f'{"ISPLATA SA RAČUNA".center(65)}\n\n{"BEZ PROVIZIJE".center(65)}\n\n')
    account_number = input("Unesite broj računa: ")

    try:
        amount = float(input("Unesite iznos za podizanje: "))
    except ValueError:
        print("Neispravan iznos.")
        return

    if account_number in accounts:
        if accounts[account_number]['balance'] >= amount:
            accounts[account_number]['balance'] -= amount
            transaction = {'date': datetime.datetime.now().date().strftime("%d.%m.%Y"),
                           'time': datetime.datetime.now().time().strftime("%H:%M"),
                           'amount': amount,
                           'description': "Isplata: " + str(amount) + " EUR"}
            accounts[account_number]['transactions'].append(transaction)
            print("Novac uspješno podignut.")
        else:
            print("Nedovoljno sredstava na računu.")
    else:
        print("Račun nije pronađen.")


def main():
    accounts = {}

    while True:
        main_menu()
        choice = input("Odaberite opciju: ")
        if choice == "1":
            open_account(accounts)
        elif choice == "2":
            display_balance(accounts)
        elif choice == "3":
            display_transactions(accounts)
        elif choice == "4":
            deposit(accounts)
        elif choice == "5":
            time_deposit(accounts)
        elif choice == "6":
            withdraw(accounts)
        elif choice == "7":
            break
        else:
            print("Nepoznata opcija. Molimo odaberite ponovno.")


if __name__ == "__main__":
    main()