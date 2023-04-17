from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class CodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Недопустимый email.'
            )
        ]
    )
    username = serializers.RegexField(regex=r'^[\w.@+-]+$')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('me - недопустимый никнейм!')
        return username

    def validate_email(self, email):
        if len(email) > 254:
            raise serializers.ValidationError('email не может быть длиннее 254 символов')
        return email
    
    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
    )
    conf_code = serializers.CharField()