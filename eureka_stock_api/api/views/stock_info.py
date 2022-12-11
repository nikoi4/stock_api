import logging

from rest_framework import status
from rest_framework.authentication import (
    TokenAuthentication,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from api.utils.integrations.alphavantage import get_alphavantage_api_response
from eureka_stock_api import settings


logger = logging.getLogger(__name__)


class StockInfo(APIView):
    """
    View to retrieve a symbol stock market information

    * Requires token authentication.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, stock_symbol):
        function = 'TIME_SERIES_DAILY_ADJUSTED'
        size = 'compact'
        api_key = settings.ALPHAVANTAGE_API_TOKEN

        logger.info('Calling alphavantage api {} for symbol --> {}'.format(
            function,
            stock_symbol
        ))
        alphavantage_response = get_alphavantage_api_response(
            function,
            api_key,
            size,
            stock_symbol,
        )
        alphavantage_response_data = alphavantage_response.json()

        if 'error' in str(alphavantage_response_data).lower():
            logger.error(alphavantage_response_data)
            return Response(
                alphavantage_response_data,
                status=status.HTTP_400_BAD_REQUEST
            )

        logger.info('Processing and transforming data into response')
        processed_data = self.process_stock_timeseries(alphavantage_response_data)
        return Response(data=processed_data, status=status.HTTP_200_OK)

    def process_stock_timeseries(self, data):
        logger.info('Getting Daily time series')
        daily_stock_info = data.get('Time Series (Daily)', {})
        if not daily_stock_info:
            raise ValidationError(detail='Non valid')

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
            'variation': str(variation),
        }

    def get_variation(self, val1, val2):
        variation = round((val1-val2)*100 / val2, 2)
        return variation
