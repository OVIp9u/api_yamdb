from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import CorrectUsername, MeUsername


User = get_user_model()


class UserAndEmailObjectsSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[MeUsername()]
    )
    email = serializers.EmailField()

    def validate_username(self, username):
        return username.lower()

    def validate_email(self, email):
        return email.lower()


class UserAndEmailModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Недопустимый email.'
            )
        ]
    )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('me - недопустимый никнейм!')

        if User.objects.filter(
            username__iexact=username.lower()
        ).exists():
            raise serializers.ValidationError(
                f'Пользователь с никнеймом {username} уже существует!'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(
            email__iexact=email.lower()
        ).exists():
            raise serializers.ValidationError(
                f'Пользователь с почтой {email} уже существует'
            )
        return email

    
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
        validators=[CorrectUsername]
    )
    conf_code = serializers.CharField()