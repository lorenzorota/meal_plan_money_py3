import os
from getpass import getpass
from connect import QPilot_Connection
from process_transactions import Transactions_Handler 

def ask_credentials():
    login_name = input("Username: ")
    password = getpass("Password: ")
    return login_name, password

def main():
    login_name, password = ask_credentials()
    qpilot_session = QPilot_Connection(login_name, password)
    qpilot_session.login()
    status = qpilot_session.get_status()

    if status.json()['loggedIn'] == True:
        print("Fetching transactions...")
        transactions = qpilot_session.get_transactions()

        sink = Transactions_Handler(transactions.json())
        sink.load()
        sink.compute()
        sink.latest()

        qpilot_session.logout()
    else:
        print("Could not login.")

if __name__ == '__main__':
    main()