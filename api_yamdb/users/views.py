from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .core import (send_mail_with_conf_code, get_access_token,
                   user_activation_token)
from .models import User
from .serializers import (TokenSerializer, UserAndEmailObjectsSerializer,
                          UserAndEmailModelSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    valid_data = dict(serializer.validated_data)
    user = get_object_or_404(
        User,
        username__iexact=valid_data['username'].lower()
    )
    if (
        user_activation_token.check_token(
            user=user,
            token=valid_data['conf_code']
        )
    ):
        token = get_access_token(user)
        return Response({'token': token['access']})
    else:
        return Response(
            {'token': 'Неверный токен!'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_conf_code(request):
    serializer = UserAndEmailObjectsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    valid_data = dict(serializer.validated_data)
    if User.objects.filter(
        **serializer.validated_data
    ).exists():
        user = User.objects.get(
            username=valid_data['username']
        )
    else:
        model_serializer = UserAndEmailModelSerializer(
            data=request.data
        )
        model_serializer.is_valid(raise_exception=True)
        user = model_serializer.save()

    send_mail_with_conf_code(
        user,
        user_activation_token.make_token(user)
    )
    return Response(serializer.data)