from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from core.signals_loader import load_signals
from core.views import handler404
from core.views import handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/",
         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/",
         TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/",
         TokenVerifyView.as_view(), name="token_verify"),
    path('api/schema/',
         SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path("media/(?P<path>.*)",
                serve, {"document_root": settings.MEDIA_ROOT})
    ]

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

load_signals()
