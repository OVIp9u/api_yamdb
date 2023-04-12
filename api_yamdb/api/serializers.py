from titles.models import Title, Category, Genre
from rest_framework import serializers
import datetime as dt




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
