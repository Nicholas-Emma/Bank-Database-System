from CitiBank_functions import *
import random as rd
from datetime import datetime as dt



class CitiBank:
    def __init__(self, access_method = None, name = None, gender = None, state_of_residence = None, dob = None, account_pin = None):
        self.isloggedin = False
        if access_method == "Log In":   #to get the customer logged in.
            #to fetch all the existing account numbers and account pins.
            with connection.cursor() as cursor:   
                query_account = "SELECT customer_id, account_no, account_pin FROM account_info;"
                cursor.execute(query_account)
                connection.commit()
                result = cursor.fetchall()

                while True:
                    ask_account_no = input("Enter account number here: ")
                    ask_account_pin = input("Enter account pin here: ")
                    #to verify details submitted
                    for entry in result:
                        if (entry["account_no"] == ask_account_no) and (entry["account_pin"] == ask_account_pin):
                            print("Login Successful")
                            self.isloggedin = True
                            self.current_customer_id = entry["customer_id"]
                            break  #to break out of the for loop
                        else:
                            pass
                    if self.isloggedin:
                        break   #to break out of the while loop(to stop asking for account number and pin)
                    else:
                        print("Incorrect details")

            #to get the customer's details from the database
            with connection.cursor() as cursor:
                query_customer = f"SELECT customer_info.full_name, customer_info.gender, customer_info.state_of_residence, customer_info.date_of_birth, account_info.account_no, account_info.account_bal, account_info.account_pin FROM customer_info INNER JOIN account_info ON customer_info.customer_id = account_info.customer_id WHERE customer_info.customer_id = {self.current_customer_id};"
                cursor.execute(query_customer)
                connection.commit()
                customer_details = cursor.fetchall()
                self.name = customer_details[0]["full_name"]
                self.gender = customer_details[0]["gender"]
                self.state_of_residence = customer_details[0]["state_of_residence"]
                self.dob = customer_details[0]["date_of_birth"]
                self.account_bal = customer_details[0]["account_bal"]
                self.account_no = customer_details[0]["account_no"]
                self.account_pin = customer_details[0]["account_pin"]
        else: #to get the customer registered
            ask_name = input("Enter name here: ").title()
            ask_gender = input("Enter gender here: ").title()
            ask_residence = input("Enter state of residence here: ").title()
            ask_dob = input("Enter date of birth here(dd/mm/yyyy): ")
            while True:  #to keep verifying the pin submitted.
                ask_pin = input("Enter a 4-digit pin here: ")
                confirm_pin = input("Enter pin again: ")
                if ask_pin == confirm_pin:
                    break
                else:
                    print("Verification failed!")
            
    
            self.name = ask_name
            self.gender = ask_gender
            self.state_of_residence = ask_residence
            splitted_date = ask_dob.split("/")
            self.dob = "-".join([splitted_date[2], splitted_date[1], splitted_date[0]])
            self.account_bal = 0
            self.account_pin = confirm_pin

            #to send the newly registered customer's details to the database.
            write_customer_info(self.name, self.gender, self.state_of_residence, self.dob)   

            #to get the customer id of the recently registered customer.
            with connection.cursor() as cursor:
                self.customer_details = "SELECT customer_id FROM customer_info;"
                cursor.execute(self.customer_details)
                connection.commit()
                result = cursor.fetchall()
                self.current_customer_id = result[-1]["customer_id"]


            #to get all the existing account numbers in order to verify the newly generated account number.
            with connection.cursor() as cursor:
                self.query = "SELECT account_no FROM account_info;"
                cursor.execute(self.query)
                connection.commit()
                if len(cursor.fetchall()) == 0:    #no existing customer.
                    self.account_no = rd.randrange(0000000000, 9999999999)
                    write_account_info(self.current_customer_id, self.account_no, self.account_bal, self.account_pin)
                else:  #existing customer(s)
                    self.list_of_account_no = []
                    #to get all the existing account numbers.
                    for entry in cursor.fetchall():
                        self.list_of_account_no.append(entry["account no"])
                    while True:
                        #to keep checking that the generated account number does not belong to an existing customer.
                        generated_no = rd.randrange(0000000000, 9999999999)
                        if generated_no in self.list_of_account_no:
                            pass
                        else:
                            self.account_no = generated_no
                            break
                    write_account_info(self.current_customer_id, self.account_no, self.account_bal, self.account_pin)
            
    
    def get_name(self):
        return self.name

    def get_account_no(self):
        return self.account_no

    def check_balance(self):
        with connection.cursor() as cursor:
            balance_query = f"SELECT account_bal FROM account_info WHERE customer_id = {self.current_customer_id};"
            cursor.execute(balance_query)
            connection.commit()
            result = cursor.fetchall()
            self.account_bal = result[0]["account_bal"]

        return f"Your account balance is: {self.account_bal}"

    def deposit(self, value):
        self.account_bal += value
        write_transaction_info(self.current_customer_id, "Credit", value, "Successful", dt.now())
        update_account(self.current_customer_id, self.account_bal)
        print("Transaction Sucessful!")

    def withdrawal(self, value):
        if self.account_bal >= value:  #to check for sufficent funds
            self.account_bal -= value
            write_transaction_info(self.current_customer_id, "Debit", value, "Successful", dt.now())
            update_account(self.current_customer_id, self.account_bal)
            print("Transaction Successful!")
        else:
            write_transaction_info(self.current_customer_id, "Debit", value, "Failed", dt.now())
            print("Insufficient Funds!")



while True:
    print("Welcome to DataBank\nEnter 1 to Login In\nEnter 2 to Sign Up")
    gain_access = input("Enter option here: ")
    if int(gain_access) == 1:   #log in
        customer = CitiBank(access_method = "Log In")
        break
    elif int(gain_access) == 2:    #sign up
        customer = CitiBank(access_method = "Sign Up")
        break
    else:
        print("Invalid response")
        print("\n")
       
print(f"Welcome {customer.get_name()} to the bank with a difference, your account number is {customer.get_account_no()}")
def menu():
    while True:
        print("\n")
        print("Enter 1 to access acount balance\nEnter 2 to make deposits\nEnter 3 to make withdrawal\nEnter 4 to quit")
        ask = int(input("Enter option here: "))
        if ask == 1:
            print(customer.check_balance())
        elif ask == 2:
            further = int(input("Enter amount here: "))
            customer.deposit(further)
        elif ask == 3:
            further = int(input("Enter amount here: "))
            customer.withdrawal(further)
        elif ask == 4:
            print("Thank you for banking with us!")
            break
        else:
            pass

menu()