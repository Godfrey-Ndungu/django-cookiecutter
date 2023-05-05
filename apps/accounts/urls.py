from django.urls import path, include
from rest_framework import routers
from .views import (
    RegistrationAPIView,
    ChangePasswordAPIView,
    ChangeProfileAPIView,
    ChangeEmailAPIView,
    CustomUserViewSet
)

router = routers.SimpleRouter()

router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path("register/",
         RegistrationAPIView.as_view(), name="register"),
    path("change_password/",
         ChangePasswordAPIView.as_view(), name="change_password"),
    path("change_profile/",
         ChangeProfileAPIView.as_view(), name="change_profile"),
    path("change_email/", ChangeEmailAPIView.as_view(), name="change_email"),
    path("", include(router.urls)),  # include the router URLs
]
