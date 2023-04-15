import datetime as dt
from rest_framework import serializers
from reviews.models import Review, Comment, Title, Category, Genre, GenreTitle
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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
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
            raise serializers.ValidationError('Проверьте год выпуска произведения!')
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
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'

# class RatingSerializer(serializers.ModelSerializer):
#     """Сериализатор рейтинга"""
#     title = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Rating
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = '__all__'
