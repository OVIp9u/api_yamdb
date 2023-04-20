import datetime as dt
import re

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Получает и добавляет категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Получает и добавляет жанры."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleReadSerializer(serializers.ModelSerializer):
    """Получает произведение."""
    genre = GenreSerializer(read_only=True, required=False, many=True)
    category = CategorySerializer(read_only=True, required=False)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score', default=0))
        return rating.get('score__avg')

    class Meta:
        fields = (
            'id', 'name', 'year',
            'description', 'genre',
            'category', 'rating'
        )
        model = Title
        order_by = ('name',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """Добавляет произведение."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError(
                'Проверьте год выпуска произведения!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def create(self, validated_data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title=validated_data.get('title')
        ).exists():
            raise serializers.ValidationError(
                'К произведению можно оставить только один отзыв'
            )
        return Review.objects.create(**validated_data)

    def validate_score(self, value):
        if 1 > value or 10 < value:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = 'username', 'email', 'first_name', 'last_name', 'bio', 'role'


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователей"""
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email и запрещает
        использовать недопустимые символы."""
        regex = re.sub(r'^[\w.@+-]+$', '', data.get('username'))
        if data.get('username') in regex:
            raise serializers.ValidationError(
                f'Имя пользователя не должно содержать {regex}'
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено'
            )
        if User.objects.filter(
            username=data.get('username'),
            email=data.get('email')
        ).exists():
            return data
        elif User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже занято!'
            )
        elif User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Данный Email уже занят!'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""

    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()
