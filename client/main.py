import requests
from getpass import getpass


OPTIONS = {
    '1': ['create user and get token', 'register/'],
    '2': ['retrieve token', 'api-token-auth/'],
    '3': ['get stock info', 'stock_info/'],
    '0': ['Exit', 'quit']
}


def run():
    # base endpoint for docker
    # base_api_endpoint = 'ht: tp://0.0.0.0:8000/api/v1/'
    # base endpoint for dev local on venv on
    base_api_endpoint = 'http://localhost:8080/api/v1/'
    print('-'*35)
    print('*** Welcome to Stock Market API ***')
    print('-'*35)

    auth_token = None

    while True:
        for option in OPTIONS.items():
            num = option[0]
            option_text = option[1][0]
            print('{} - {}'.format(num, option_text))

        user_option = input("\nSelect api action\n")

        # Non actionable
        if not OPTIONS.get(user_option, ''):
            print('Invalid option')
            continue

        if user_option == '0':
            print('See you soon!!')
            break

        selected_option = OPTIONS[user_option][1]
        endpoint = '{}{}'.format(base_api_endpoint, selected_option)

        # User Related actions
        if user_option in ['1', '2']:
            data = {
                'username': input('User Name: '),
                'password': getpass('User Password: ')
            }
            if user_option == '1':
                data.update({
                        'email': input('Email: '),
                        'first_name': input('User First Name: '),
                        'last_name': input('User Last Name: '),
                })
            response = requests.post(endpoint, json=data)
            if response.status_code in [200, 201]:
                auth_token = response.json().get('token', '')

        # Stock related actions
        # Require authentication
        if user_option == '3':
            symbol = input('Input desired stock symbol: ')
            stock_info_url = '{}{}'.format(endpoint, symbol)
            headers = {'Authorization': 'Token {}'.format(auth_token)}

            response = requests.get(stock_info_url, headers=headers)

        print('\nResponse --> {}\n'.format(response.json()))


if __name__ == '__main__':
    run()
