import requests
from getpass import getpass


OPTIONS = {
    '1': ['get/retrieve token', 'api-token-auth/'],
    '2': ['get hello world', 'hello/'],
    '0': ['Exit', 'quit']
}


def run():
    # base_docker_api_endpoint = 'http://0.0.0.0:8000/api/v1/'
    base_docker_api_endpoint = 'http://localhost:8080/api/v1/'
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
        selected_option = OPTIONS[user_option][1]
        if selected_option == OPTIONS['0'][1]:
            print('See you soon!!')
            break
        endpoint = '{}{}'.format(base_docker_api_endpoint, selected_option)
        if selected_option == OPTIONS['1'][1]:
            user = input('User Name:   ')
            password = getpass('User Password:   ')
            data = {'username': user, 'password': password}
            response = requests.post(endpoint, json=data)
            if response.status_code == 200:
                auth_token = response.json().get('token', '')
        else:
            headers = {'Authorization': 'Token {}'.format(auth_token)}
            response = requests.get(endpoint, headers=headers)

        print('\nResponse --> {}\n'.format(response.json()))


if __name__ == '__main__':
    run()
