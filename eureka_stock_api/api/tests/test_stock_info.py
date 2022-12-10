import requests
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


BASE_API_URL = '/api/v1/'


class StockInfoTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user({
            'username': 'foo',
            'password': 'bar',
        })
        self.endpoint = '{}stock_info/'.format(BASE_API_URL)
        self.client.force_authenticate(user=self.user)

    @patch('requests.models.Response.json')
    @patch('api.views.stock_info.get_alphavantage_api_response')
    def test_get_stock_info_is_valid(self, alphavantage_api_mock, mock_response_json):
        alphavantage_response = requests.models.Response()
        alphavantage_response.status_code = status.HTTP_200_OK
        alphavantage_api_mock.return_value = alphavantage_response
        mock_response_json.return_value = {
            'Meta Data': {
                '1. Information': 'Daily Time Series with Splits and Dividend Events',
                '2. Symbol': 'meta',
                '3. Last Refreshed': '2022-12-09',
                '4. Output Size': 'Compact',
                '5. Time Zone': 'US/Eastern'
            },
            'Time Series (Daily)': {
                '2022-12-08': {
                    '1. open': '116.39',
                    '2. high': '117.34',
                    '3. low': '114.59',
                    '4. close': '115.33',
                    '5. adjusted close': '115.33',
                    '6. volume': '30619418',
                    '7. dividend amount': '0.0000',
                    '8. split coefficient': '1.0'
                },
                '2022-12-07': {
                    '1. open': '113.76',
                    '2. high': '115.88',
                    '3. low': '112.88',
                    '4. close': '113.93',
                    '5. adjusted close': '113.93',
                    '6. volume': '29461137',
                    '7. dividend amount': '0.0000',
                    '8. split coefficient': '1.0'
                },
                '2022-12-09': {
                    '1. open': '115.3',
                    '2. high': '117.54',
                    '3. low': '113.87',
                    '4. close': '115.9',
                    '5. adjusted close': '115.9',
                    '6. volume': '26033353',
                    '7. dividend amount': '0.0000',
                    '8. split coefficient': '1.0'
                }
            }
        }
        # using only required fields
        endpoint = '{}meta'.format(self.endpoint)
        # force_authenticate(request, user=self.user)
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'higher_price': '117.54',
            'lower_price': '113.87',
            'open_price': '115.3',
            'variation': '0.49'
        }

    def test_get_stock_info_is_not_authorized(self):
        self.client.force_authenticate()
        # using only required fields
        endpoint = '{}meta'.format(self.endpoint)
        # force_authenticate(request, user=self.user)
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data.get('detail').code == 'not_authenticated'

    @patch('requests.models.Response.json')
    @patch('api.views.stock_info.get_alphavantage_api_response')
    def test_get_stock_info_is_not_valid(self, alphavantage_api_mock, mock_response_json):
        alphavantage_response = requests.models.Response()
        alphavantage_response.status_code = status.HTTP_200_OK
        alphavantage_api_mock.return_value = alphavantage_response
        mock_response_json.return_value = {
            'Error Message': 'Invalid API call. Please retry or visit the documentation (https://www.alphavantage.co/documentation/) for TIME_SERIES_DAILY_ADJUSTED.'
        }
        # using only required fields
        endpoint = '{}meta'.format(self.endpoint)
        # force_authenticate(request, user=self.user)
        response = self.client.get(endpoint)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == mock_response_json.return_value
