import requests

from rest_framework.authentication import (
    TokenAuthentication,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from eureka_stock_api import settings


class StockInfo(APIView):
    """
    View to retrieve a symbol stock market information

    * Requires token authentication.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, stock_symbol):
        function = 'TIME_SERIES_DAILY_ADJUSTED'
        size = 'compact'
        api_key = settings.ALPHAVANTAGE_API_TOKEN

        response = self.get_alphavantage_api_response(
            function,
            stock_symbol,
            size,
            api_key
        )
        if response.status_code == 200:
            data = self.process_stock_timeseries(response.json())
            return Response(data=data, status=200)

        return Response(
            response.json(),
            status=response.status_code
        )

    def get_alphavantage_api_response(
            self,
            function,
            stock_symbol,
            size,
            api_key
    ):
        endpoint = 'https://www.alphavantage.co/query'
        query_params = '?function={}&symbol={}&outputsize={}&apikey={}'.format(
            function,
            stock_symbol,
            size,
            api_key,
        )
        return requests.get('{}{}'.format(endpoint, query_params))

    def process_stock_timeseries(self, data):
        daily_stock_info = data.get('Time Series (Daily)', {})
        if not daily_stock_info:
            # TODO replace by exception
            return {}

        available_days = list(daily_stock_info.keys())
        last_day = max(available_days)
        available_days.remove(last_day)
        previous_day = max(available_days)

        last_stock_day = daily_stock_info.get(last_day, {})
        previous_stock_day = daily_stock_info.get(previous_day, {})

        last_closing = float(last_stock_day.get('4. close'))
        previous_closing = float(previous_stock_day.get('4. close'))
        variation = self.get_variation(last_closing, previous_closing)

        return {
            'open_price': last_stock_day.get('1. open', ''),
            'higher_price': last_stock_day.get('2. high', ''),
            'lower_price': last_stock_day.get('3. low', ''),
            'variation': variation,
        }

    def get_variation(self, val1, val2):
        variation = round((val1-val2)*100 / val2, 2)
        return variation
