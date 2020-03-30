# Meal plan money checker (python3 prototype)

## Description

The purpose of this program is to display how much meal plan money one has on their account at Jacobs University Bremen, and to display the transaction history (authentication via the QPilot API).

>Note: The program is still in development, and is ultimately not intended for practical use (an iOS and android app will be developed later).

## Setup

1. Make sure that you have *python* version >= 3.6, equipped with *pip*
2. Install *pipenv* (through your favorite package manager) <sup id="a1">[1](#pipenv)</sup>

    macOS:

    ``` bash
    brew install pipenv
    ```

    Ubuntu 17.10:

    ```bash
    sudo apt install software-properties-common python-software-properties
    sudo add-apt-repository ppa:pypa/ppa
    sudo apt update
    sudo apt install pipenv
    ```

    Alternative:

    ```bash
    pip install pipenv
    ```

3. Install the dependencies for this project by running the following in the parent directory:

    ```bash
    pipenv install
    ```

## Usage

1. If you have not registered your QPilot credentials, do so by running the following:

    ```bash
    $ pipenv run python register.py
    Enter your jacobs e-mail: [e-mail here]
    Enter your campus card number: [password here]
    ```

    You will receive an e-mail from the QPilot server, which instructs you on how to setup your password

2. To run the program enter the following:

    ```bash
    $ pipenv run python runner.py
    Username: [username here]
    Password: [password here]
    Fetching transactions...
    ----------------------------------------
    Current meal-plan money: € xxx.xx
    Last updated: xxxx-xx-xx xx:xx:xx+01:00
    ----------------------------------------

    ```

3. Incase the displayed balance is incorrect, you can set a fixed offset by running the `[-c]` calibration option:

    ```bash
    $ pipenv run python runner.py -c
    Username: [username here]
    Password: [password here]
    Calibration factor: [offset here]
    Fetching transactions...
    ----------------------------------------
    Current meal-plan money: € xxx.xx
    Last updated: xxxx-xx-xx xx:xx:xx+01:00
    ----------------------------------------
    ```

    The calibration factor can be reset at any point in time and will remain stored in the `data.json` configuration file.

    > Note: The balance may be computed incorrectly in the event that the user's transaction history does not contain particular transactions (due to a server outage).

<b id="pipenv">1</b> [Link] (https://pipenv-es.readthedocs.io/es/stable/) [↩](#a1)
