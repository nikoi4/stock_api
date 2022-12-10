import requests


def get_alphavantage_api_response(
    function,
    api_key,
    size,
    stock_symbol,
):
    endpoint = 'https://www.alphavantage.co/query'
    query_params = '?function={}&symbol={}&outputsize={}&apikey={}'.format(
        function,
        stock_symbol,
        size,
        api_key,
    )
    return requests.get('{}{}'.format(endpoint, query_params))
