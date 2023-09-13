import json
import os.path

users_list = []

def load_users():
    global users_list
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users_list = json.load(f)
    else:
        users_list = []

def save_users():
    with open("users.json", "w") as f:
        json.dump(users_list, f, indent=2)

def register():
    name = input("Enter your name: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    gender = input("Enter your gender: ")
    age = int(input("Enter your age: "))
    city = input("Enter your city: ")
    balance = float(input("Enter your starting balance (in EGP): "))
    password = input("Enter your password: ")

    user_dict = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "gender": gender,
        "age": age,
        "city": city,
        "balance": balance,
        "password": password
    }

    users_list.append(user_dict)
    save_users()

    print("Your account has been created successfully. Your ID is", len(users_list) - 1)

def login():
    id = input("Enter your ID: ")
    password = input("Enter your password: ")
    try:
     user_id = int(id)
     if user_id < len(users_list) and users_list[user_id]["password"] == password:
         while True:
            print("0. Deposit")
            print("1. Transfer")
            print("2. Withdraw")
            print("3. Check personal information")
            print("4. Check balance")
            print("5. Reset password")
            print("6. Exit")
            choice = input("Enter your choice (0-6): ")

            if choice == "0":
                deposit(int(id))

            elif choice == "1":
                transfer(int(id))

            elif choice == "2":
                withdraw(int(id))

            elif choice == "3":
                show_personal_information(int(id))

            elif choice == "4":
                show_balance(int(id))

            elif choice == "5":
                reset_password(int(id))

            elif choice == "6":
                print("Thank you for using the SIC Bank Management System!")
                break

            else:
                print("Invalid input. Please try again.")

     elif int(id) < len(users_list) and users_list[int(id)]["password"] != password:
        reset_choice = input("Invalid password. Do you want to reset your password? (y/n): ")

        if reset_choice == "y":
            reset_password(int(id))
        else:
             print("Please try again with the correct password.")
     else:

        print("Invalid ID or password. Please try again.")


    except ValueError:

        print("Invalid ID. Please enter a valid ID.")
def convert_currency(amount, from_currency, to_currency):
    conversion_rates = {"USD": 30, "SAR": 9, "EGP": 1}
    converted_amount = amount * (conversion_rates[from_currency] / conversion_rates[to_currency])
    return converted_amount

def deposit(user_id):
    amount = float(input("Enter the amount you want to deposit: "))

    while True:
        currency = input("Enter the currency (USD, SAR, or EGP): ")
        if currency in ["USD", "SAR", "EGP"]:
            break
        else:
            print("Invalid currency. Please enter a valid currency.")

    amount_egp = convert_currency(amount, currency, "EGP")

    users_list[user_id]["balance"] += amount_egp
    print("Your deposit of", amount, currency, "has been processed successfully.")
    print("Your balance is", users_list[user_id]["balance"], "EGP")
    save_users()

def transfer(user_id):
    amount = float(input("Enter the amount you want to transfer: "))
    to_id = input("Enter the ID of the account you want to transfer to: ")

    try:
        to_id = int(to_id)
        if to_id >= len(users_list):
            print("Invalid ID. Please try again.")
            return

        if users_list[user_id]["balance"] >= amount:
            users_list[user_id]["balance"] -= amount
            users_list[to_id]["balance"] += amount
            to_name = users_list[to_id]["name"]
            to_balance = users_list[to_id]["balance"]
            print("Your transfer of", amount, "EGP to", to_name, "has been processed.")
            save_users()
            print("Your balance now is", users_list[user_id]["balance"], "EGP.")
        else:
            print("Insufficient balance.")

    except ValueError:
        print("Invalid ID. Please enter a valid ID.")
def withdraw(user_id):
    amount = float(input("Enter the amount you want to withdraw: "))

    while True:
        currency = input("Enter the currency (USD, SAR, or EGP): ")
        if currency in ["USD", "SAR", "EGP"]:
            break
        else:
            print("Invalid currency. Please enter a valid currency.")

    amount_egp = convert_currency(amount, currency, "EGP")

    if users_list[user_id]["balance"] >= amount_egp:
        users_list[user_id]["balance"] -= amount_egp
        print("Your withdrawal of", amount, currency, "has been processed successfully.")
        print("Your balance is", users_list[user_id]["balance"], "EGP")
        save_users()
    else:
        print("Insufficient balance.")
def show_personal_information(user_id):
    user = users_list[user_id]
    print("Name:", user["name"])
    print("Phone Number:", user["phone_number"])
    print("Email:", user["email"])
    print("Gender:", user["gender"])
    print("Age:", user["age"])
    print("City:", user["city"])
    print(" balance: ", users_list[user_id]["balance"], "EGP")

def show_balance(user_id):
    print("Your balance is", users_list[user_id]["balance"], "EGP")

def reset_password(user_id):
    new_password = input("Enter your new password: ")
    users_list[user_id]["password"] = new_password
    print("Your password has been reset successfully.")
    save_users()

load_users()

while True:
    print("0. Register")
    print("1. Login")
    print("2. Exit")
    choice = input("Enter your choice (0-2): ")
    if choice == "0":
        register()

    elif choice == "1":
        login()

    elif choice == "2":
        print("Thank you for using the SIC Bank Management System!")
        break

    else:
        print("Invalid input. Please try again.")