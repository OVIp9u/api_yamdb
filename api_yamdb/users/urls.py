from .views import get_conf_code, get_token
from django.urls import include, path

urlpatterns = [
    path('auth/', include(
        [
            path('signup/', get_conf_code, name='get_conf_code'),
            path('token/', get_token, name='get_token'),
        ]
    ))
]
