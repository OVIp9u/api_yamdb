from http.client import HTTPException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework import viewsets, status
from reviews.models import Review, Comment, Title, Genre, Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer, UserSerializer
from rest_framework import viewsets
from django.db.models import Avg
from .serializers import TitleReadSerializer, TitleWriteSerializer, CategorySerializer, GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведений."""
    queryset = Title.objects.all()
    # serializer_class = TitleReadSerializer
    # queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleWriteSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Title.objects.all()

        return Title.objects.all().annotate(rating=Avg('reviews__score'))


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзыва"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Метод выбора комментариев по отзыву"""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        """Метод создания комментария"""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


# class RatingViewSet(viewsets.ModelViewSet):
#     """Вьюсет рейтинга"""
#     serializer_class = RatingSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     def get_queryset(self):
#         """Метод выбора рейтинга по произведению"""
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, pk=title_id)
#         rating = title.annotate(score = Avg('reviews__score'))
#         return rating


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей"""
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
