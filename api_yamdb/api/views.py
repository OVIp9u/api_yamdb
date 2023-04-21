from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters_df
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import SERVICE_EMAIL
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (
    IsAdminIsModeratorIsAuthor, IsAdminRole,
    IsAdminUserOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer, SignUpSerializer,
    TitleReadSerializer, TitleWriteSerializer,
    TokenSerializer, UserSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведений."""
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
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


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Вьюсет Категорий произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Вьюсет Жанров произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly | IsAdminRole]


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзыва"""
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    permission_classes = [IsAdminIsModeratorIsAuthor, ]

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

    permission_classes = [IsAdminIsModeratorIsAuthor, ]

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
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

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


def code_generation_and_sender(user):
    """Функция создает код подтверждения и отправляет
    письмо с ним на почту пользователя"""
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()
    title = 'Код авторизации Yamdb.'
    message = (f'Здравствуйте, {user}!'
               f'Ваш код подтверждения {code}')
    from_mail = SERVICE_EMAIL
    user_mail = [user.email]
    return send_mail(title, message, from_mail, user_mail)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Функция получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data.get("username")
    )
    if serializer.validated_data.get(
        "confirmation_code"
    ) == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения!'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Функция регистрации пользователей"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    code_generation_and_sender(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
