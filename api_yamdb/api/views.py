from titles.models import Title, Genre, Category
from rest_framework import viewsets

from .serializers import TitleSerializer, CategorySerializer, GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        categories = Category.objects.filter(slug=category_slug)
        for category in categories:
            serializer.validated_data['category'] = category

        genre_slug = self.request.data['genre']
        serializer.validated_data['genre'] = []
        for slug in genre_slug:
            genres = Genre.objects.filter(slug=slug)
            for genre in genres:
                serializer.validated_data['genre'].append(genre)

        serializer.save()

    def perform_update(self, serializer):
        if 'category' in self.request.data:
            category_slug = self.request.data['category']
            categories = Category.objects.filter(slug=category_slug)
            for category in categories:
                serializer.validated_data['category'] = category

        if 'genre' in self.request.data:
            genre_slug = self.request.data['genre']
            serializer.validated_data['genre'] = []
            for slug in genre_slug:
                genres = Genre.objects.filter(slug=slug)
                for genre in genres:
                    serializer.validated_data['genre'].append(genre)

        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
