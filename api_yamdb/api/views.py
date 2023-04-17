from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied, ValidationError
from users.models import User

from rest_framework.filters import SearchFilter
from rest_framework import viewsets, status
from django.shortcuts import render
from reviews.models import Review, Comment

from rest_framework import viewsets, status, filters
from reviews.models import Review, Comment, Title, Genre, Category
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .serializers import CommentSerializer, ReviewSerializer, UserSerializer
from rest_framework import viewsets
from django.db.models import Avg
from .serializers import TitleReadSerializer, TitleWriteSerializer, CategorySerializer, GenreSerializer
from django_filters import rest_framework as filters_df
from .filters import TitleFilter
from .serializers import CategorySerializer, GenreSerializer

from .permissions import IsAdminRole, IsAdminUserOrReadOnly, IsModeratorRole, ObjectPermissions, IsUserRole
from .permissions import IsAdminUserOrReadOnly, IsUserRole, IsAdminRole, IsModeratorRole


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведений."""
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
'''
    def get_queryset(self):
        """Добавляет рейтинг Произведению при GET запросе."""
        if self.action in ('list', 'retrieve'):
            return Title.objects.annotate(avg_rating=Avg('reviews__score'))
        return Title.objects.all()
'''

class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
