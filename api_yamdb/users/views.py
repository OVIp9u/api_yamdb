from random import randint

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import SERVICE_EMAIL

from .models import User
from .serializers import CodeSerializer, TokenSerializer


def conf_code_generator(user):
    code = randint(100000, 999999)
    user.confirmation_code = code
    user.save()
    title = 'Код авторизации Yamdb.'
    message = (f'Здравствуйте, {user}!'
               f'Ваш код подтверждения {code}')
    from_mail = SERVICE_EMAIL
    user_mail = [user.email]
    return send_mail(title, message, from_mail, user_mail)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get("username")
    )
    if serializer.validated_data.get("confirmation_code") == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_conf_code(request):
    serializer = CodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        user, _ = User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        errors = (
            f"Имя {username} уже используется"
            if User.objects.filter(username=username).exists()
            else f"Email {email} уже используется"
        )
        return Response(errors, status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        user = get_object_or_404(User, username=username)
        if user.email != email:
            return Response(
                {'Некорректный email!'}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        User.objects.create_user(username=username, email=email)
    user = get_object_or_404(User, email=email)
    conf_code_generator(user)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )
