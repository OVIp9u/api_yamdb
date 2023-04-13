from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class CorrectUsername(validators.RegexValidator):
    """Валидатор соответсвия никнейма с допустимыми символами"""
    regex = r'^[a-z][a-z0-9_]+$'
    message = ('Неправильное имя пользователя.'
               ' Допустимы только: латиница, числа, подчёркивания'
    )
    flags = 0


@deconstructible
class MeUsername(validators.RegexValidator):
    """Валидатор для Username != Me"""
    regex = r'^(?!Me$|me$|ME$|mE$).*$'
    message = ('Имя пользователя не должно быть - Me')
    flags = 0