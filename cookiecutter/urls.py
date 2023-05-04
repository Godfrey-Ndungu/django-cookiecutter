from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("login/token/",
         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token/refresh/",
         TokenRefreshView.as_view(), name="token_refresh"),
    path("login/token/verify/",
         TokenVerifyView.as_view(), name="token_verify"),
    path('api/schema/',
         SpectacularAPIView.as_view(), name='schema'),
    path('documentation/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path("media/(?P<path>.*)",
                serve, {"document_root": settings.MEDIA_ROOT})
    ]

handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
