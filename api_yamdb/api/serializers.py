import datetime as dt
import re

from django.shortcuts import get_object_or_404
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
    rating = serializers.IntegerField(read_only=True)

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
        """Проверка года выпуска произведения"""
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

    def validate(self, data):
        """Запрет публикации больше одного отзыва"""
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_exists = Review.objects.filter(
            author=author,
            title=title
        ).exists()
        if request.method == 'POST' and review_exists:
            raise serializers.ValidationError(
                'К произведению можно оставить только один отзыв'
            )
        return data

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
        """Запрещает пользователям повторно использовать
        username и email."""
        current_username = data.get('username')
        current_email = data.get('email')
        if User.objects.filter(
            username=current_username,
            email=current_email
        ).exists():
            return data
        elif User.objects.filter(username=current_username).exists():
            raise serializers.ValidationError(
                'Данное имя пользователя уже занято!'
            )
        elif User.objects.filter(email=current_email).exists():
            raise serializers.ValidationError(
                'Данный Email уже занят!'
            )
        return data

    def validate_username(self, value):
        """Запрещает пользователям присваивать себе имя me
        и использовать недопустимые символы."""
        regex = re.sub(r'^[\w.@+-]+$', '', value)
        if value in regex:
            raise serializers.ValidationError(
                f'Имя пользователя не должно содержать {regex}'
            )
        elif value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена"""
    username = serializers.CharField(
        max_length=150,
    )
    confirmation_code = serializers.CharField()
