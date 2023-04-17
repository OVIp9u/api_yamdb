from django.shortcuts import get_object_or_404, render
from django_filters import rest_framework as filters_df
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
import rest_framework.mixins
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (IsAdminRole, IsAdminUserOrReadOnly,
                          ObjectPermissions)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)




class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведений."""
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]
    queryset = Title.objects.all()
    filter_backends = (filters_df.DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    ordering_fields = ('name', 'rating')

    def get_serializer_class(self):
        """Меняет сериалайзер POST/PUT/PATCH запросов
        для передачи поля slug.
        """
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer

        return TitleWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]

    def retrieve(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]

    def retrieve(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(self.request.data, status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзыва"""
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ObjectPermissions,]

    def get_queryset(self):
        """Метод выбора отзыва по произведению"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        """Метод создания отзыва"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [ObjectPermissions,]

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
    permission_classes = [IsAdminRole]
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
