from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request, *args, **kwargs):
    return Response({"message": "Hello world"})
