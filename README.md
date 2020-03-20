# Meal plan money checker (python3 prototype)

## Description

The purpose of this program is to display how much meal plan money one has on their account at Jacobs University Bremen, and to display the transaction history (authentication via the QPilot API).

>Note: The program is still in development, and is ultimately not intended for practical use (an iOS and android app will be developed later).

## Setup

1. Make sure that you have *python* version >= 3.7, equipped with *pip*
2. Install *pipenv* (through your favorite package manager) [^pipenv]
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

1. (Linux / macOS) Set up your credentials (of your QPilot user, NOT campusnet) as *environment* variables in the following manner:

    ```bash
    unset HISTFILE
    export LOGIN_NAME=name_here
    export LOGIN_PASSWORD=password_here
    ```

2. The hard work is done, to run the program enter the following:

    ```bash
    pipenv run python runner.py
    ```

[^pipenv]: [Link] (https://pipenv-es.readthedocs.io/es/stable/)