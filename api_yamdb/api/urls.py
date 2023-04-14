from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TitleViewSet, CategoryViewSet, GenreViewSet, UserViewSet, CommentViewSet, ReviewViewSet
from rest_framework.authtoken import views

router = DefaultRouter()

router.register('categories', CategoryViewSet)

router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
router.register('users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('auth/', include('users.urls')),
    #path('', include(router.urls)),    
]
