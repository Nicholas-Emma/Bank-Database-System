import pymysql
from pymysql import cursors

###CONNECTING TO THE DATABASE IN SQL
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    db = "citiBank",
    charset = "utf8mb4",
    cursorclass = pymysql.cursors.DictCursor
)



##WRITING FUNCTION TO CREATE TABLES
def create_tables():
    with connection.cursor() as cursor:
        add_customer_table = """
                    CREATE TABLE IF NOT EXISTS customer_info(
                        customer_id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY,
                        Full_name VARCHAR(40) NOT NULL,
                        Gender VARCHAR (10) NOT NULL,
                        State_of_Residence VARCHAR(20) NOT NULL,
                        date_of_Birth DATE NOT NULL
                    );
        """
        cursor.execute(add_customer_table)
        connection.commit()

        add_transaction_table = """
                       CREATE TABLE IF NOT EXISTS transaction_info(
                           transaction_id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY,
                           customer_id INT(10) NOT NULL,
                           FOREIGN KEY transaction_info(customer_id) REFERENCES customer_info(customer_id),
                           transaction_type VARCHAR(20) NOT NULL,
                           Amount INT(10) DEFAULT 0,
                           Status VARCHAR(20) NOT NULL,
                           date_and_time DATETIME
                        ); 
        """
        cursor.execute(add_transaction_table)
        connection.commit() 

        add_account_table = """
                    CREATE TABLE IF NOT EXISTS account_info(
                        account_id INT(10) AUTO_INCREMENT NOT NULL PRIMARY KEY,
                        customer_id INT(10) NOT NULL,
                        FOREIGN KEY account_info(customer_id) REFERENCES customer_info(customer_id),
                        account_no VARCHAR(10) NOT NULL,
                        account_bal BIGINT(15) NOT NULL,
                        account_pin VARCHAR(4) NOT NULL
                    );
        """   

        cursor.execute(add_account_table)
        connection.commit()

##FUNCTION THAT WRITE INTO THE CUSTOMER_INFO TABLE
def write_customer_info(current_name, current_gender, current_residence, current_dob):
    with connection.cursor() as cursor:
        add_data = f"""
            INSERT INTO customer_info(Full_name, Gender, State_of_Residence, date_of_Birth)
            VALUES
            ('{current_name}', '{current_gender}', '{current_residence}', '{current_dob}');
        """
        cursor.execute(add_data)
        connection.commit()

##FUNCTION THAT WRITE INTO THE TRANSACTION_INFO TABLE
def write_transaction_info(current_custid, current_type, current_amount, current_status, current_dt):
    with connection.cursor() as cursor:
        add_data = f"""
            INSERT INTO transaction_info(customer_id, transaction_type, Amount, Status, date_and_time)
            VALUES
            ('{current_custid}','{current_type}','{current_amount}','{current_status}','{current_dt}');
        """    
        cursor.execute(add_data)
        connection.commit()

##FUNCTION THAT INTO THE ACCOUNT_INFO TABLE
def write_account_info(cust_id, account_no, account_bal, account_pin):
    with connection.cursor() as cursor:
        add_data = f"""
            INSERT INTO account_info(customer_id, account_no, account_bal, account_pin)
            VALUES
            ('{cust_id}','{account_no}','{account_bal}','{account_pin}');
        """
        cursor.execute(add_data)
        connection.commit()

##FUNCTION THAT UPDATES ACCOUNT BALANCES
def update_account(current_custid, account_bal):
    with connection.cursor() as cursor:
        update_data = f"UPDATE account_info SET account_bal = {account_bal} WHERE customer_id = {current_custid};"
        cursor.execute(update_data)
        connection.commit()


create_tables()

