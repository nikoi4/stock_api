import requests
from getpass import getpass


OPTIONS = {
    '1': ['create user and get token', 'register/'],
    '2': ['retrieve token', 'api-token-auth/'],
    '3': ['get hello world', 'hello/'],
    '0': ['Exit', 'quit']
}


def run():
    # base endpoint for docker
    base_api_endpoint = 'http://0.0.0.0:8000/api/v1/'
    # base endpoint for local
    # base_api_endpoint = 'http://localhost:8080/api/v1/'
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
        if user_option == '0':
            print('See you soon!!')
            break
        if not OPTIONS.get(user_option, ''):
            print('Invalid option')

        selected_option = OPTIONS[user_option][1]
        endpoint = '{}{}'.format(base_api_endpoint, selected_option)
        if user_option in ['1', '2']:
            if user_option == '1':
                data = {
                    'username': input('User Name: '),
                    'email': input('Email: '),
                    'first_name': input('User First Name: '),
                    'last_name': input('User Last Name: '),
                    'password': getpass('User Password: ')
                }
            if user_option == '2':
                data = {
                    'username': input('User Name: '),
                    'password': getpass('User Password: ')
                }
            response = requests.post(endpoint, json=data)
            if response.status_code in [200, 201]:
                auth_token = response.json().get('token', '')
        else:
            headers = {'Authorization': 'Token {}'.format(auth_token)}
            response = requests.get(endpoint, headers=headers)

        print('\nResponse --> {}\n'.format(response.json()))


if __name__ == '__main__':
    run()
