import os
import json
import argparse
from getpass import getpass
from connect import QPilot_Connection
from process_transactions import Transactions_Handler
from pathlib import Path

def load_config(filename:str, username: str) -> dict:
    with open(filename, 'r') as file:
        data = json.load(file)
        user_data = data['user_data']
        for user in user_data:
            if user['username'] == username:
                return user

def user_modify(data: dict, username: str, **attr: dict):
    for user in data:
        if user['username'] == username:
            for key, value in attr.items():
                user[key] = value

def user_exists(data: dict, username: str) -> bool:
    for user in data:
        if user['username'] == username:
            return True
    return False

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

def create_config():
    data = json.loads('{"user_data": []}')
    write_json(data, 'data.json')

def update_config(username: str, calibration=None):
    file = Path("./data.json")
    if not file.is_file():
        create_config()

    with open('data.json') as json_file:
        data = json.load(json_file)
        if 'user_data' not in data:
            return

        user_data = data['user_data']
        if not user_exists(user_data, username):
            if calibration is None:
                calibration = 0.0
            user = {'username': username,
                    'calibration': calibration
                    }
            user_data.append(user)
        elif calibration is not None:
            user_modify(user_data, username, calibration=calibration)

    write_json(data, 'data.json')

def ask_credentials():
    login_name = input("Username: ")
    password = getpass("Password: ")
    return login_name, password

def main():
    parser = argparse.ArgumentParser(description='Display the available meal plan money for an individual at Jacobs University Bremen')
    parser.add_argument('-c', action='store_true', default=False,
                        dest='boolean_calibrate',
                        help='set the calibration factor (default: 0.0)')

    args = parser.parse_args()
    login_name, password = ask_credentials()
    qpilot_session = QPilot_Connection(login_name, password)
    qpilot_session.login()
    status = qpilot_session.get_status()

    if status.json()['loggedIn'] == True:
        # set calibration
        if args.boolean_calibrate:
            calibration = input("Calibration factor: ") or None
            if calibration is not None:
                calibration = float(calibration)
            update_config(login_name, calibration)
        else:
            update_config(login_name)

        # load user configuration
        config = load_config('data.json', login_name)
        calibration = config['calibration']

        # handle transactions
        print("Fetching transactions...")
        transactions = qpilot_session.get_transactions()

        sink = Transactions_Handler(transactions.json(), calibration)
        sink.load()
        sink.compute()
        sink.latest()

        qpilot_session.logout()
    else:
        print("Could not login.")

if __name__ == '__main__':
    main()