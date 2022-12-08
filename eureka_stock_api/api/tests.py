import pytest

from django.contrib.auth.models import User
from rest_framework.authtoken import views as auth_views
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory

from api.views import UserView


BASE_API_URL = 'api/v1/'


@pytest.mark.django_db
def test_post_register_returns_api_token():
    # using only required fields
    view = UserView.as_view()
    new_user = {
        'username': 'foo',
        'email': 'foo@bar.com',
        'password': 'very_secret_password',

    }
    factory = APIRequestFactory()
    request = factory.post(
        '{}register/'.format(BASE_API_URL),
        new_user,
        format='json'
    )
    response = view(request)

    assert response.data.get('token')
    assert response.status_code == 201


@pytest.mark.django_db
def test_invalid_email_post_register():
    # using only required fields
    view = UserView.as_view()
    new_user = {
        'username': 'foo',
        'email': 'foobar',
        'password': 'very_secret_password',

    }
    factory = APIRequestFactory()
    request = factory.post(
        '{}register/'.format(BASE_API_URL),
        new_user,
        format='json'
    )
    response = view(request)

    assert response.exception is True
    assert response.data.get('email', [])[0].code == 'invalid'
    assert response.status_code == 400


@pytest.mark.django_db
def test_invalid_method_get_register():
    # using only required fields
    view = UserView.as_view()
    new_user = {
        'username': 'foo',
        'email': 'foobar',
        'password': 'very_secret_password',

    }
    factory = APIRequestFactory()
    request = factory.get(
        '{}register/'.format(BASE_API_URL),
        new_user,
        format='json'
    )
    response = view(request)

    assert response.exception is True
    assert response.data.get('detail').code == 'method_not_allowed'
    assert response.status_code == 405


@pytest.mark.django_db
def test_post_retrieve_api_token_for_existing_user():
    # using only required fields
    view_function = auth_views.obtain_auth_token
    existing_user = {
        'username': 'foo',
        'email': 'foo@bar.com',
        'password': 'very_secret_password',
    }
    user = User.objects.create_user(**existing_user)
    token = Token.objects.create(user=user)

    factory = APIRequestFactory()
    request = factory.post(
        '{}api-token-auth/'.format(BASE_API_URL),
        existing_user,
        format='json'
    )
    response = view_function(request)

    assert response.data.get('token') == str(token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_user_retrieve_api_token_for_non_existing_user():
    # using only required fields
    view_function = auth_views.obtain_auth_token
    non_existing_user = {
        'username': 'bar',
        'password': 'not_very_secret',
    }

    factory = APIRequestFactory()
    request = factory.post(
        '{}api-token-auth/'.format(BASE_API_URL),
        non_existing_user,
        format='json'
    )
    response = view_function(request)

    assert response.exception is True
    assert response.data.get('non_field_errors', [])[0].code == 'authorization'
    assert response.status_code == 400


@pytest.mark.django_db
def test_invalid_method_get_retrieve_api_token_returns_error():
    # using only required fields
    view_function = auth_views.obtain_auth_token
    non_existing_user = {
        'username': 'bar',
        'password': 'not_very_secret',
    }

    factory = APIRequestFactory()
    request = factory.get(
        '{}api-token-auth/'.format(BASE_API_URL),
        non_existing_user,
        format='json'
    )
    response = view_function(request)

    assert response.exception is True
    assert response.data.get('detail').code == 'method_not_allowed'
    assert response.status_code == 405
