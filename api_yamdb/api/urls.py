from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()

router.register('categories', CategoryViewSet)

router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
]
