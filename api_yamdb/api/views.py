from http.client import HTTPException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from titles.models import Title, Genre, Category
from users.models import User
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from django.shortcuts import render
from reviews.models import Review, Comment
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer, UserSerializer
from rest_framework import viewsets
from django.db.models import Avg
from .serializers import TitleSerializer, CategorySerializer, GenreSerializer
from .permissions import IsAdminRole, IsAdminUserOrReadOnly, IsModeratorRole, ObjectPermissions, IsUserRole


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly,]

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
    permission_classes = [IsAdminUserOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзыва"""
    serializer_class = ReviewSerializer
    permission_classes = (ObjectPermissions,)

    def get_queryset(self):
        """Метод выбора отзыва по произведению"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Метод создания отзыва"""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""
    serializer_class = CommentSerializer
    #permission_classes = (IsAdminRole | IsModeratorRole | IsObjectOwner)

    def get_queryset(self):
        """Метод выбора комментариев по отзыву"""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Метод создания комментария"""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей"""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    #permission_classes = [IsAdminRole]
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    
    @action(
        methods=['patch', 'get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
