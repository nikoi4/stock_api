import logging

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from api import serializers


logger = logging.getLogger(__name__)


class UserView(generics.CreateAPIView):
    """
    View to Register a new user in the system assigning
    the user an api token

    * Any user can access this endpoint
    """

    serializer_class = serializers.UserSerializer
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create user
        logger.info('Registering user {}'.format(serializer.data.username))
        user = self.perform_create(serializer)
        # create token for user
        logger.info('Assigning Token to user')
        token = Token.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'token': str(token)},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return User.objects.create_user(**serializer.data)
