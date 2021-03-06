import json
import os
import pytz
import re
from getpass import getpass
from datetime import datetime
from connect import QPilot_Connection 

class Transactions_Handler():
    ''' Store and process the transaction log of the user '''

    def __init__(self, source: json, calibration=0.0):
        ''' Initialize all objects '''
        self.transaction_json = source

        ''' Format of table per item:
            0 date
            1 transaction_number
            2 is_apetito_trxn
            3 is_duplicate
            4 amount_delta
            5 old_balance
            6 new_balance
            7 apetito_balance
        '''
        self.data_buffer = [[] for _ in range(len(source))]
        self.german_tz = pytz.timezone("Europe/Berlin")
        self.calibration = calibration

    def is_servery_trxn(self, i: int) -> bool:
        amount = self.data_buffer[i][4]
        old_bal = self.data_buffer[i][5]
        new_bal = self.data_buffer[i][6]
        
        # base case
        if i == 0:
            return True if (old_bal == None) else False
        else:
            new_bal_prev = self.data_buffer[i-1][6]
            if  not (new_bal - new_bal_prev) == amount \
                and old_bal == None:
                return True
            else:
                return False

    def is_duplicate(self, i: int) -> bool:
        date_str = self.data_buffer[i][0]
        amount = self.data_buffer[i][4]
        txn_no = self.data_buffer[i][1]

        # base case
        if i == 0:
            return False
        else:
            date_str_prev = self.data_buffer[i-1][0]
            amount_prev = self.data_buffer[i-1][4]
            txn_no_prev = self.data_buffer[i-1][1]
            if  date_str == date_str_prev \
                and amount == amount_prev \
                and txn_no == txn_no_prev:
                return True
            else:
                return False

    def load(self):
        for i, item in enumerate(self.transaction_json):
            # fitler out ISO formatted date up until period
            date_str = re.search('(.*)\\.', item['logDate']).group(1)

            # store date object with timezone + dst
            # date = self.german_tz.localize(datetime.fromisoformat(date_str))

            self.data_buffer[i].append(date_str)
            self.data_buffer[i].append(item['transactionNumber'])
            self.data_buffer[i].append(0)
            self.data_buffer[i].append(0)

            # correct the raw data into more useful data
            self.data_buffer[i].append(
                0 if item['amount'] == None else \
                -1*item['amount'] if item['oldBalance'] == None else item['amount'] 
                )
            self.data_buffer[i].append(
                None if item['oldBalance'] == None else -1*item['oldBalance']
                )
            self.data_buffer[i].append(
                -1*item['newBalance'] if item['newBalance'] != 0.0 else 0.0
                )
            self.data_buffer[i].append(0)
        self.data_buffer.reverse()

        # remove old or corrupted logs (before the year 2015)
        i = 0
        while int(re.search('[^-]*', self.data_buffer[i][0]).group(0)) < 2015:
            self.data_buffer.pop(i)

    def compute(self):
        for i, item in enumerate(self.data_buffer):
            item[2] = is_servery_trxn = self.is_servery_trxn(i)
            item[3] = is_duplicate = self.is_duplicate(i)
            # base case: total balance is the added starting amount
            if i == 0:
                item[7] = item[4]
            elif is_servery_trxn and not is_duplicate:
                # check that we are not subtracting what we added when maxing out
                if abs(self.data_buffer[i-1][4]) == 12.66 and item[4] == -12.66:
                    item[4] = 0
                # only add value that does not overflow maximum allowance (180)
                if item[4] + self.data_buffer[i-1][7] <= 180:
                    item[7] = item[4] + self.data_buffer[i-1][7]
                # if it does not overflow, make sure it does not underflow (0)
                elif item[4] + self.data_buffer[i-1][7] <= 0:
                    item[7] = 0
                # if value is ambiguous assume it reached the maximum allowance
                else:
                    item[7] = 180
            # copy the total balance from the previous transaction
            else:
                item[7] = self.data_buffer[i-1][7]

        # apply calibration factor to the computed balance
        if self.calibration + self.data_buffer[-1][7] <= 180:
            self.data_buffer[-1][7] = self.calibration + self.data_buffer[-1][7]
        elif self.calibration + self.data_buffer[-1][7] <= 0:
            self.data_buffer[-1][7] = 0
        else:
            self.data_buffer[-1][7] = 180

    def latest(self):
        date = self.german_tz.localize(datetime.fromisoformat(self.data_buffer[-1][0]))
        print("----------------------------------------")
        print("Current meal-plan money: € {0:.2f}".format(self.data_buffer[-1][7]))
        print("Last updated: {}".format(date))
        print("----------------------------------------")

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
        print("Raw JSON:")
        print(json.dumps(transactions.json(), indent=2))

        sink = Transactions_Handler(transactions.json())
        sink.load()
        sink.compute()
        print("Processed data:")
        for item in sink.data_buffer:
            print(item)

        qpilot_session.logout()
    else:
        print("Could not login.")

if __name__ == '__main__':
    main()