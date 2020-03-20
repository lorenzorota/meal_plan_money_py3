import os
from connect import QPilot_Connection
from process_transactions import Transactions_Handler 

login_name = os.environ['LOGIN_NAME']
password = os.environ['LOGIN_PASSWORD']

def main():
    qpilot_session = QPilot_Connection(login_name, password)
    qpilot_session.login()

    print("Fetching transactions...")
    transactions = qpilot_session.get_transactions()

    sink = Transactions_Handler(transactions.json())
    sink.load()
    sink.compute()
    sink.latest()

    qpilot_session.logout()

if __name__ == '__main__':
    main()