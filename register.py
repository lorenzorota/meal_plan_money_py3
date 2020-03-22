import requests 
import json
import os

URL = 'https://qpilot.jacobs-university.de:1081/api'

class QPilot_Connection():
    ''' Connection class for handling authentication and extraction of QPilot data '''

    def __init__(self, email: str, card_number: str):
        ''' Initialize all objects '''
        self.email = email
        self.card_number = card_number
        self.client = requests.session()

    def register(self) -> requests:
        ''' Start session (store cookies) '''
        try:
            self.client.get(URL)

            # generate the csrf token
            csrf_token = self.client.cookies['XSRF-TOKEN'] 

            # login to service
            payload = {'mailAddress': self.email, 'cardNumber': self.card_number}
            headers = {'Content-Type': 'application/json','X-XSRF-TOKEN': csrf_token}
            result = self.client.post(url=URL + '/account/password-recovery/send-instructions', data=json.dumps(payload), headers=headers) 
        except json.decoder.JSONDecodeError:
            print("Login error HTTP code: {}".format(result.status_code))
        else:
            return result


def main():
    email = input("Enter your jacobs e-mail: ")
    card_number = input("Enter your campus card number: ")
    qpilot_session = QPilot_Connection(email, card_number)
    status = qpilot_session.register()

    if status.status_code == 204:
        print("Check your inbox for a password recovery link.")
    else:
        print("The e-mail and card number do not correspond, try again.")

if __name__ == '__main__':
    main()
