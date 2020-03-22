import requests
import json
from getpass import getpass
import os

URL = 'https://qpilot.jacobs-university.de:1081/api'

class QPilot_Connection():
    ''' Connection class for handling authentication and extraction of QPilot data '''

    def __init__(self, login_name: str, password: str):
        ''' Initialize all objects '''
        self.login_name = login_name
        self.password = password
        self.client = requests.session()

    def login(self):
        ''' Start session (store cookies) '''
        try:
            self.client.get(URL)

            # generate the csrf token
            csrf_token = self.client.cookies['XSRF-TOKEN'] 

            # login to service
            payload = {'loginName': self.login_name, 'password': self.password}
            headers = {'Content-Type': 'application/json','X-XSRF-TOKEN': csrf_token}
            result = self.client.post(url=URL + '/session', data=json.dumps(payload), headers=headers) 
        except json.decoder.JSONDecodeError:
            print("Login error HTTP code: {}".format(result.status_code))

    def logout(self):
        ''' Close current session '''
        try:
            self.client.get(URL)

            # fetch the csrf token
            csrf_token = self.client.cookies['XSRF-TOKEN'] 

            # logout from service
            payload = {'loginName': self.login_name, 'password': self.password}
            headers = {'Accept': 'application/json, text/plain, */*','X-XSRF-TOKEN': csrf_token}
            result = self.client.delete(url=URL + '/session', data=json.dumps(payload), headers=headers)

            self.client.close()
        except json.decoder.JSONDecodeError:
            print("Logout error HTTP code: {}".format(result.status_code))

    def get_status(self) -> requests:
        ''' Fetch current login status from api '''
        try:
            result = self.client.get(url=URL + '/session')
        except:
            print("Something went wrong here")
        else:
            return result

    def get_transactions(self) -> requests:
        ''' Fetch user's transactions from api '''
        try:
            result = self.client.get(url=URL + '/transactions')
        except:
            print("Something went wrong here")
        else:
            return result

def ask_credentials():
    login_name = input("Username: ")
    password = getpass("Password: ")
    return login_name, password

def main():
    login_name, password = ask_credentials()
    qpilot_session = QPilot_Connection(login_name, password)
    qpilot_session.login()
    
    #transactions = qpilot_session.get_transactions()
    #with open('transactions.json', 'w+') as out_file:
    #    json.dump(transactions.json(), out_file)

    status = qpilot_session.get_status()

    print("HTTP response: {}".format(status.status_code))
    print(json.dumps(status.json(), indent=2))
    qpilot_session.logout()

if __name__ == '__main__':
    main()
