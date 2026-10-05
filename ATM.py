import string
import json
import bcrypt
import random
import re

def log_action(func):
    def wrapper(username):
        result = func(username)

        entry = {
            "username": username,
            "action": func.__name__
        }

        try:
            with open("logs.json", "r") as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []

        logs.append(entry)

        with open("logs.json", "w") as file:
            json.dump(logs, file, indent=4)

        return result

    return wrapper

def load_users():
    try:
        with open("clients.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        users = {
            "users": [],
            "loan_requests": []
        }
        with open("clients.json", "w") as file:
            json.dump(users, file, indent=4)

def save_users(users):
    with open("clients.json", "w") as file:
        json.dump(users, file, indent=4)

def hashed_pass(password):
    bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def generate_account_number():
    digits = ''.join(random.choices(string.digits, k=18))
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"GE{digits[:2]}{letters}{digits[2:]}"

def register():
    first_name = input("Enter your first name: ").strip().capitalize()
    last_name = input("Enter your last name: ").strip().capitalize()

    users = load_users()

    while True:
        username = input("Enter your Username: ").strip()
        if any(user["username"] == username for user in users["users"]):
            print("Username is already taken. Please choose another one.")
            continue
        break

    while True:
        password = input("Enter password: ")
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
        if re.match(pattern, password):
            print("Password is valid")
            break
        else:
            print("Password is not valid.")
            continue

    hashed_password = hashed_pass(password)
    bank_iban = generate_account_number()

    new_user = {
        "firstname" : first_name,
        "lastname" : last_name,
        "username" : username,
        "password" : hashed_password,
        "balance" : {
        '₾' : 0,
        '$' : 0,
        '€' : 0
        },
        "Account Number" : bank_iban,
        "role" : "client"
    }
    users["users"].append(new_user)

    save_users(users)

    return username

def login():
    while True:
        username = input("Enter your username: ").strip()
        users = load_users()

        for user in users["users"]:
            if user["username"] == username:
                break
        else:
            print("Username doesn't exist")
            continue

        while True:
            password = input("Enter your password: ")
            if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                code = "".join(random.choices(string.digits, k=4))
                print(f'Your verification code is {code}')
                verification_code = input("Enter the code: ").strip()
                if code == verification_code:
                    print("Logged in successfully")
                    return user
                else:
                    print("Wrong code")
                    continue
            else:
                print("Wrong password")
                continue

def check_balance(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username:
            print("Your balances:")
            for currency, amount in user["balance"].items():
                print(f"{currency}: {amount}")
            return user["balance"]
    print("Username not found")
@log_action
def deposit(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username:
            currency = input("Choose the currency(₾, $, €): ").strip()
            if currency not in user["balance"]:
                print("Invalid currency.")
                return
            try:
                dep = float(input("Enter the amount of money: "))
            except ValueError:
                print("Please enter a valid number")
                return
            if dep <= 0:
                print("Amount must be more than 0")
                return

            user["balance"][currency] += dep
            new_balance = user["balance"][currency]

            save_users(users)

            print(f"Deposit was successful. Deposited {dep}{currency}. Current balance: {new_balance}{currency}")

            return user["balance"]

    print("Username not found")
@log_action
def withdraw(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username:
            currency = input("Choose the currency(₾, $, €): ").strip()
            if currency not in user["balance"]:
                print("Invalid currency.")
                return
            try:
                withd = float(input("Enter the amount of money: "))
            except ValueError:
                print("Please enter a valid number.")
                return
            if withd <= 0:
                print("Amount must be more than 0")
                return
            if withd > user["balance"][currency]:
                print("There's not enough money on balance")
                return

            user["balance"][currency] -= withd

            save_users(users)

            print(f"Withdrew {withd}{currency}. Balance: {user['balance'][currency]}{currency}")
            return user["balance"]

    print("Username not found")
@log_action
def transaction(username):
    users = load_users()
    sender = None
    for user in users["users"]:
        if username == user["username"]:
            sender = user
    if sender is None:
        print("Username not found")
        return

    acc_number = input("Enter the Account number: ").strip()
    for user in users["users"]:
        if user["Account Number"] == acc_number:
            if user is sender:
                print("You cannot send money to yourself")
                return
            currency = input("Choose the currency(₾, $, €): ").strip()
            if currency not in sender["balance"]:
                print("Invalid currency.")
                return
            try:
                amount = float(input("How much would you like to send: "))
            except ValueError:
                print("Please enter a valid number")
                return
            if amount <= 0:
                print("Amount must be more than 0")
                return
            if amount > sender["balance"][currency]:
                print("There's not enough money on balance")
                return

            user["balance"][currency] += amount
            sender["balance"][currency] -= amount

            save_users(users)

            print("Money has been sent")
            return sender["balance"]
    print("Account number not found")
@log_action
def convert(username):
    rates = {
    "₾": {
        "$": 0.3836,
        "€": 0.3396
    },
    "$": {
        "₾": 2.6000,
        "€": 0.8834
    },
    "€": {
        "₾": 2.9250,
        "$": 1.1220
    }
}

    users = load_users()

    for user in users["users"]:
        if user["username"] == username:
            sell_curr = input("Select the currency you want to exchange from (₾, $, €): ").strip()
            buy_curr = input("Select the currency you want to exchange to (₾, $, €): ").strip()

            if sell_curr not in user["balance"]:
                print("Invalid currency.")
                return
            if buy_curr not in user["balance"]:
                print("Invalid currency.")
                return
            if sell_curr == buy_curr:
                print("You cannot exchange the same currency")
                return
            try:
                amount = float(
                    input("Enter the amount of money you want to exchange: ")
                )
            except ValueError:
                print("Please enter a valid number")
                return

            if amount <= 0:
                print("Amount must be more than 0")
                return

            if amount > user["balance"][sell_curr]:
                print("There's not enough money on balance")
                return

            rate = rates[sell_curr][buy_curr]

            user["balance"][sell_curr] -= amount

            converted_amount = round(amount * rate, 2)
            user["balance"][buy_curr] += converted_amount

            save_users(users)

            print(f"Exchanged {amount}{sell_curr} to {converted_amount}{buy_curr}")
            return user["balance"]

    print("Username not found")

def request_loan(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username:
            currency = input("Select the currency for the loan: ").strip()
            if currency not in user["balance"]:
                print("Invalid currency.")
                return
            try:
                amount = float(input("Enter the amount: "))
                months = int(input("Enter the period (months): "))
            except ValueError:
                print("Please enter a valid number.")
                return
            if amount <= 0:
                print("Amount must be more than 0.")
                return
            if months <= 0:
                print("Period must be more than 0.")
                return

            rate = 8
            total = amount * (1 + rate / 100)
            new_loan = {
                "username" : username,
                "amount" : amount,
                "currency" : currency,
                "months" : months,
                "monthly_payment" : round(total / months, 2),
                "rate" : rate,
                "status" : "pending"
            }
            users["loan_requests"].append(new_loan)

            save_users(users)

            print("Loan request submitted")
            return new_loan

    print("Username not found")

def check_loan_status(username):
    users = load_users()

    loans = []
    for loan in users["loan_requests"]:
        if loan["username"] == username:
            loans.append(loan)

    if not loans:
        print("There is no loan request under your name")
        return
    print(f'Loan status: {loans[-1]["status"]}')
    return loans[-1]["status"]

def loan_review(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username and user["role"] == "admin":
            print("Admin access granted")
            break
    else:
        print("You are not an admin")
        return

    for loan in users["loan_requests"]:
        if loan["status"] != "pending":
            continue
        print(loan)
        decision = input("Accept or Reject the loan request: ").lower().strip()
        if decision == "accept":
            for user in users["users"]:
                if user["username"] == loan["username"]:
                    user["balance"][loan["currency"]] += loan["amount"]
                    loan["status"] = "Accepted"
                    print("Loan accepted")
                    break

        elif decision == "reject":
            loan["status"] = "Rejected"
            print("Loan rejected")
    save_users(users)

def show_users(username):
    users = load_users()

    for user in users["users"]:
        if user["username"] == username and user["role"] == "admin":
            print("All users:")
            for user in users["users"]:
                print("\nFirst name:", user["firstname"])
                print("Last name:", user["lastname"])
                print("Username:", user["username"])
                print("Balance:", user["balance"])
                print("Account Number:", user["Account Number"])
                print("Role:", user["role"])

            return

    print("You are not an admin")


def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            username = register()
            if username:
                print(f"Account created for {username}. You can log in now.")

        elif choice == "2":
            user = login()
            if user is None:
                continue
            username = user["username"]
            is_admin = user.get("role") == "admin"

            while True:
                print("\n1. Check balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Send money")
                print("5. Convert currency")
                print("6. Request a loan")
                print("7. Check loan status")
                if is_admin:
                    print("8. Review loan requests")
                    print("9. Show Clients")
                print("0. Log out")
                action = input("Choose an option: ").strip()

                if action == "1":
                    check_balance(username)
                elif action == "2":
                    deposit(username)
                elif action == "3":
                    withdraw(username)
                elif action == "4":
                    transaction(username)
                elif action == "5":
                    convert(username)
                elif action == "6":
                    request_loan(username)
                elif action == "7":
                    check_loan_status(username)
                elif action == "8" and is_admin:
                    loan_review(username)
                elif action == "9" and is_admin:
                    show_users(username)
                elif action == "0":
                    print("Logged out")
                    break
                else:
                    print("Invalid option.")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()