from titles.models import Title, Category, Genre
from rest_framework import serializers
import datetime as dt
from rest_framework import serializers
from reviews.models import Review, Comment, Rating
from users.models import User
from django.shortcuts import get_object_or_404

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
    genre = GenreSerializer(required=False)
    # genre = serializers.SlugRelatedField(
    #     many=True,
    #     slug_field='name',
    #     queryset=Genre.objects.all()
    # )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
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

    def validate_score(self, value):
        if 1>value or 10<value:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, value):
        request = self.context['request']
        author = request.user
        id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=id)
        if request.method == 'Post' and Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError('К произведению можно оставить только один отзыв')


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