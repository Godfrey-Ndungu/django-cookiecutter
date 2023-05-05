from rest_framework import generics, permissions, status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

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
        password = serializer.validated_data.get("password")
        is_superuser = serializer.validated_data.get("is_superuser", False)

        if is_superuser:
            user = CustomUser.objects.create_superuser(
                email=email, password=password)
        else:
            user = CustomUser.objects.create_user(
                email=email, password=password)

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

    @action(detail=False, methods=['GET'])
    def list_accounts(self, request):
        """
        List all CustomUsers
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'PUT', 'PATCH', 'POST'])
    def account_details(self, request, pk=None):
        """
        Retrieve, update or create a CustomUser
        """
        user = self.get_object()

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH', 'POST']:
            serializer = self.get_serializer(user,
                                             data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
