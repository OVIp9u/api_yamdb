from titles.models import Title, Category, Genre
from rest_framework import serializers
import datetime as dt
from rest_framework import serializers
from reviews.models import Review, Comment, Rating
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, required=False, many=True)
    category = CategorySerializer(read_only=True, required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        order_by = ('name',)

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

class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор рейтинга"""
    title = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    class Meta:
        model = User
        fields = '__all__'