from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.views import RegistrationAPIView
from apps.accounts.models import CustomUser


class RegistrationAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_user_registration_success(self):
        data = {
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "is_superuser": False
        }

        url = reverse("register")
        request = self.factory.post(url, data, format="json")
        response = RegistrationAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=data["email"])
        self.assertEqual(user.phone_number, data["phone_number"])
        self.assertTrue(user.check_password(data["password"]))

    def test_registration_missing_email(self):
        data = {
            "phone_number": "1234567890",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "is_superuser": False
        }

        url = reverse("register")
        request = self.factory.post(url, data, format="json")
        response = RegistrationAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_phone_number(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "is_superuser": False
        }

        url = reverse("register")
        request = self.factory.post(url, data, format="json")
        response = RegistrationAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_missing_password(self):
        data = {
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "confirm_password": "testpassword",
            "is_superuser": False
        }

        url = reverse("register")
        request = self.factory.post(url, data, format="json")
        response = RegistrationAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_confirm_password(self):
        data = {
            "email": "testuser@example.com",
            "phone_number": "1234567890",
            "password": "testpassword",
            "is_superuser": False
        }

        url = reverse("register")
        request = self.factory.post(url, data, format="json")
        response = RegistrationAPIView.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_passwords_do_not_match(self):
        data = {
            "email": "testuserpassword@example.com",
            "phone_number": "+2545666666",
            "password": "testpasword1",
            "confirm_password": "non-matchng password",
        }

        request = self.factory.post(reverse("register"), data, format="json")
        response = RegistrationAPIView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that no user was created
        self.assertEqual(CustomUser.objects.count(), 0)


class ChangePasswordAPIViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            email='user@test.com',
            password='testpass123',
        )
        activate_user = CustomUser.objects.get(email="user@test.com")
        activate_user.is_active = True
        activate_user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_change_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        url = reverse('change_password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newtestpass123',
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'message': 'Password changed successfully'})

    def test_change_password_invalid_old_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        url = reverse('change_password')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newtestpass123',
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {"non_field_errors": ["Incorrect password."]})

    def test_change_password_unauthorized(self):
        url = reverse('change_password')
        data = {
            'old_password': 'testpass123',
            'new_password': 'newtestpass123',
        }

        response = self.client.put(url, data, format="json")
        """
        The ChangePasswordAPIView is using the permission class
        permissions.IsAuthenticated which allows access only
        to authenticated users. If an unauthenticated user tries to
        access this view, they will receive a 403 Forbidden response.
        """
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChangeProfileAPIViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            email='user@test.com',
            password='testpass123',
        )
        activate_user = CustomUser.objects.get(email="user@test.com")
        activate_user.is_active = True
        activate_user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_change_phone_number(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'phone_number': '+1234567890'}
        url = reverse('change_profile')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('phone_number'), '+1234567890')

    def test_unauthenticated_request(self):
        data = {'phone_number': '+1234567890'}
        url = reverse('change_profile')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_no_phone_number(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {}
        url = reverse('change_profile')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_phone_number(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'phone_number': ''}
        url = reverse('change_profile')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChangeEmailAPIViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            email='user@test.com',
            password='testpass123',
        )
        activate_user = CustomUser.objects.get(email="user@test.com")
        activate_user.is_active = True
        activate_user.save()

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_change_email(self):
        url = reverse('change_email')
        data = {'email': 'user@example.com'}
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'message': 'Email address changed successfully'})

    def test_change_email_unauthorized(self):
        url = reverse('change_email')
        data = {'email': 'user@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_email_bad_request(self):
        url = reverse('change_email')
        data = {'email': 'invalid_email'}
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)


class CustomUserViewSetTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        # create a superuser
        self.superuser = CustomUser.objects.create_superuser(
            email='superuser@test.com',
            password='testpass123',
        )
        activate_user = CustomUser.objects.get(email="superuser@test.com")
        activate_user.is_active = True
        activate_user.save()

        # create a regular user
        self.user = CustomUser.objects.create_user(
            email='user@test.com',
            password='testpass123',
        )
        activate_user = CustomUser.objects.get(email="user@test.com")
        activate_user.is_active = True
        activate_user.save()

        # get refresh token for superuser
        self.refresh = RefreshToken.for_user(self.superuser)
        self.access_token = str(self.refresh.access_token)

    def test_list_accounts(self):
        """
        Test that a superuser can list all CustomUser objects
        """
        url = reverse('users-list')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_accounts_non_superuser(self):
        """
        Test that a non-superuser cannot list all CustomUser objects
        """
        url = reverse('users-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_details(self):
        """
        Test that a superuser can retrieve,
        update or create a CustomUser object
        """
        url = reverse('users-account-details', kwargs={'pk': self.user.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_account_details_non_superuser(self):
        """
        Test that a non-superuser cannot retrieve,
        update or create a CustomUser object
        """
        url = reverse('users-account-details', kwargs={'pk': self.user.pk})
        data = {'email': 'newuser@test.com'}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_details_nonexistent_user(self):
        """
        Test that a superuser cannot retrieve a nonexistent CustomUser object
        """
        url = reverse('users-account-details', kwargs={'pk': 999})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
