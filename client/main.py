import requests


OPTIONS = {
    '1': ['get hello world', 'hello/'],
    '0': ['Exit', 'quit']
}


def run():
    base_api_endpoint = 'http://0.0.0.0:8000/api/v1/'
    print('Welcome to Stock Market API')
    while True:
        for option in OPTIONS.items():
            num = option[0]
            option_text = option[1][0]
            print('{} - {}'.format(num, option_text))
        user_option = input("Select action\n")
        selected_option = OPTIONS[user_option][1]
        if selected_option == OPTIONS['0'][1]:
            print('See you soon!!')
            break
        endpoint = '{}{}'.format(base_api_endpoint, selected_option)
        response = requests.get(endpoint)
        print(response.json())


if __name__ == '__main__':
    run()
