from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb.settings import SERVICE_EMAIL

from .models import User
from .serializers import (TokenSerializer,
                          CodeSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    conf_code = serializer.validated_data.get('conf_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, conf_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK
            )
    else:
        return Response(
            {'confitrmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_conf_code(request):
    serializer = CodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if any((
            User.objects.filter(username=username).exists(),
            User.objects.filter(email=email).exists()
    )):
        return Response(
            {"Такое имя пользователя или e-mail уже используется."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        User.objects.create_user(username=username, email=email)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    mail_subject = 'Код подтверждения для сервиса yamdb'
    send_mail(mail_subject, message, SERVICE_EMAIL, [email])
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )