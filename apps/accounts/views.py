from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ChangeProfileSerializer,
    ChangeEmailSerializer,
)


class RegistrationAPIView(generics.CreateAPIView):
    """
    API view for user registration.
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


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
            serializer.save()
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
        serializer = self.serializer_class(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Email address changed successfully"},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
