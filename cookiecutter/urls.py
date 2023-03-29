from django.contrib import admin
from django.urls import path, re_path,include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += [
        re_path("media/(?P<path>.*)", serve,
                {"document_root": settings.MEDIA_ROOT})
    ]
