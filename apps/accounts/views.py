from rest_framework import generics, permissions, status, viewsets, filters
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ChangeProfileSerializer,
    ChangeEmailSerializer,
    CustomUserSerializer
)


class RegistrationAPIView(generics.CreateAPIView):
    """
    API view for user registration.
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Create a new user and return a response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone_number = serializer.validated_data.get("phone_number", "")
        password = serializer.validated_data.get("password")
        is_superuser = serializer.validated_data.get("is_superuser", False)

        if is_superuser:
            with transaction.atomic():
                user = CustomUser.objects.create_superuser(
                    email=email, phone_number=phone_number, password=password
                )
        else:
            with transaction.atomic():
                user = CustomUser.objects.create_user(
                    email=email, phone_number=phone_number, password=password
                )

        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED, headers=headers
        )

    def get_response_data(self, user):
        """
        Get the response data for a successful registration.
        """
        return {"email": user.email}


class ChangePasswordAPIView(APIView):
    """
    API view for changing user's password.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeProfileAPIView(generics.UpdateAPIView):
    """
    API view for changing user's profile.
    """

    serializer_class = ChangeProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangeEmailAPIView(APIView):
    """
    API view for changing user's email address.
    """

    serializer_class = ChangeEmailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"email": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"email": ["Enter a valid email address."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        user.email = email
        user.save()
        return Response(
            {"message": "Email address changed successfully"},
            status=status.HTTP_200_OK
        )


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows viewing, updating, and creating CustomUsers
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['phone_number', 'email', 'is_active', 'is_staff']
    ordering_fields = ['email', 'date_joined']
