from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils import six
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import SERVICE_EMAIL


def send_mail_with_conf_code(user, conf_code):
    send_mail(
        subject=f'Код авторизации для {user}',
        message=(
            f'{user}, ваш код авторизации - {conf_code}'
        ),
        from_email=SERVICE_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


user_activation_token = TokenGenerator()


def get_access_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }