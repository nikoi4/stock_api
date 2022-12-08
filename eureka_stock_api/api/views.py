from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication
)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api import serializers


@api_view(["GET"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request, *args, **kwargs):
    return Response({"message": "Hello world"})


class UserView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create user
        user = self.perform_create(serializer)
        # create token for user
        token = Token.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'token': str(token)},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return User.objects.create_user(**serializer.data)
