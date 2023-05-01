from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.accounts.models import CustomUser
from apps.accounts.models import UserVisitHistory
from apps.accounts.models import LoginHistoryTrail
from apps.accounts.models import LoginAttemptsHistory
from apps.accounts.models import ExtraData
from apps.accounts.models import OTP


class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpass"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.phone_number, "")
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com", password="superpass"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        email = "testuser@example.com"
        password = "testpass"
        user = CustomUser.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, "")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(password))

        # Test that creating a user with no email raises a ValueError
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="")

    def test_create_superuser(self):
        email = "superuser@example.com"
        password = "superpass"
        superuser = CustomUser.objects.create_superuser(
            email=email, password=password)
        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.phone_number, "")
        self.assertFalse(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))


class UserVisitHistoryModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@example.com")

    def test_create_user_visit_history(self):
        visit = UserVisitHistory.objects.create(
            user=self.user,
            url="/test",
            referer="http://example.com/",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
        )

        self.assertEqual(visit.user, self.user)
        self.assertEqual(visit.url, "/test")
        self.assertEqual(visit.referer, "http://example.com/")
        self.assertEqual(
            visit.user_agent,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
        )
        self.assertLess((timezone.now() - visit.timestamp).seconds, 5)

    def test_user_visit_history_ordering(self):
        # Create visits with different timestamps
        visit1 = UserVisitHistory.objects.create(
            user=self.user,
            url="/test1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
            timestamp=timezone.now() - timezone.timedelta(days=1),
        )
        visit2 = UserVisitHistory.objects.create(
            user=self.user,
            url="/test2",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",  # noqa
            timestamp=timezone.now(),
        )

        # Ensure that the visits are returned in the correct order
        visits = UserVisitHistory.objects.filter(user=self.user)
        self.assertQuerysetEqual(
            visits, [visit2.pk, visit1.pk],
            transform=lambda x: x.pk, ordered=True
        )


class LoginHistoryTrailTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="password"
        )

    def test_create_login_history_trail(self):
        login_history = LoginHistoryTrail.objects.create(
            user=self.user,
            timestamp=timezone.now(),
            successful=True,
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
            location="Test Location",
        )
        self.assertEqual(LoginHistoryTrail.objects.count(), 1)
        self.assertEqual(login_history.user, self.user)
        self.assertTrue(login_history.successful)
        self.assertEqual(login_history.ip_address, "127.0.0.1")
        self.assertEqual(login_history.user_agent, "Mozilla/5.0")
        self.assertEqual(login_history.location, "Test Location")

    def test_ordering(self):
        login_history_1 = LoginHistoryTrail.objects.create(
            user=self.user,
            timestamp=timezone.now(),
            successful=True,
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
        )
        login_history_2 = LoginHistoryTrail.objects.create(
            user=self.user,
            timestamp=timezone.now() + timezone.timedelta(minutes=1),
            successful=True,
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
        )
        self.assertEqual(list(LoginHistoryTrail.objects.all()),
                         [login_history_2, login_history_1])


class LoginAttemptsHistoryTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@example.com")

    def test_create_login_attempt(self):
        ip_address = "127.0.0.1"
        user_agent = "Mozilla/5.0"
        login_attempt = LoginAttemptsHistory.objects.create(
            user=self.user, ip_address=ip_address, user_agent=user_agent
        )
        self.assertEqual(login_attempt.user, self.user)
        self.assertAlmostEqual(
            login_attempt.timestamp, timezone.now(),
            delta=timezone.timedelta(seconds=1))
        self.assertFalse(login_attempt.successful)
        self.assertEqual(login_attempt.ip_address, ip_address)
        self.assertEqual(login_attempt.user_agent, user_agent)


class ExtraDataTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@example.com")

    def test_create_extra_data(self):
        browser = "Firefox"
        ip_address = "127.0.0.1"
        device = "iPhone"
        os = "iOS"
        location = "New York"
        extra_data = ExtraData.objects.create(
            user=self.user, browser=browser, ip_address=ip_address,
            device=device, os=os, location=location
        )
        self.assertEqual(extra_data.user, self.user)
        self.assertAlmostEqual(extra_data.timestamp, timezone.now(),
                               delta=timezone.timedelta(seconds=1))
        self.assertEqual(extra_data.browser, browser)
        self.assertEqual(extra_data.ip_address, ip_address)
        self.assertEqual(extra_data.device, device)
        self.assertEqual(extra_data.os, os)
        self.assertEqual(extra_data.location, location)


class OTPModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            password="password",
            email="johndoe@example.com",
        )

    def test_create_new_otp_for_user(self):
        # create an OTP for the user
        otp = OTP.create(user=self.user)

        # assert that the OTP is for the correct user
        self.assertEqual(otp.user, self.user)

        # assert that the OTP code is a 4-digit number
        self.assertTrue(otp.code.isdigit())
        self.assertEqual(len(otp.code), 4)

        # assert that the OTP is active
        self.assertTrue(otp.active)

        # assert that the OTP was created
        self.assertIsNotNone(otp.created_at)

        # assert that the OTP was updated
        self.assertIsNotNone(otp.updated_at)

        # assert that no other OTPs for the user are active
        self.assertFalse(OTP.objects.filter(
            user=self.user, active=True).exclude(id=otp.id).exists())

    def test_create_multiple_otps_for_user(self):
        # create two OTPs for the user
        otp1 = OTP.create(user=self.user)
        otp2 = OTP.create(user=self.user)

        # assert that the OTPs are for the correct user
        self.assertEqual(otp1.user, self.user)
        self.assertEqual(otp2.user, self.user)

        # assert that the OTP codes are unique
        self.assertNotEqual(otp1.code, otp2.code)

        # assert that the OTPs are active
        self.assertTrue(otp1.active)
        self.assertTrue(otp2.active)

        # assert that the OTPs were created
        self.assertIsNotNone(otp1.created_at)
        self.assertIsNotNone(otp2.created_at)

        # assert that the OTPs were updated
        self.assertIsNotNone(otp1.updated_at)
        self.assertIsNotNone(otp2.updated_at)

        # assert that no other OTPs for the user are active
        self.assertFalse(
            OTP.objects.filter(user=self.user, active=True).exclude(
                id__in=[otp1.id, otp2.id]).exists()
        )

    def test_create_otp_with_invalid_code(self):
        with self.assertRaises(ValidationError):
            # create an OTP with an invalid code
            otp = OTP.create(user=self.user)
            otp.code = 'abcd'
            otp.save()

    def test_create(self):
        otp = OTP.create(self.user)

        self.assertTrue(otp.is_valid())
        self.assertEqual(otp.user, self.user)

        otp2 = OTP.create(self.user)
        self.assertNotEqual(otp.code, otp2.code)

        otp3 = OTP.create(self.user)
        self.assertFalse(
            OTP.objects.filter(
                user=self.user,
                active=True).exclude(
                id=otp3.id).exists())

    def test_invalid_otp_code(self):
        otp = OTP.create(self.user)

        with self.assertRaises(ValidationError):

            otp.code = '123'
            otp.save()

    def test_get_latest(self):
        OTP.create(self.user)
        OTP.create(self.user)
        otp3 = OTP.create(self.user)

        latest_otp = OTP.get_latest(self.user)
        self.assertEqual(latest_otp, otp3)

        latest_otp = OTP.get_latest(self.user)
        self.assertEqual(latest_otp, otp3)

    def test_is_valid(self):
        OTP.create(self.user)
        otp = OTP.objects.get(user=self.user, active=True)

        self.assertTrue(otp.is_valid())

        otp.updated_at = otp.updated_at - \
            timezone.timedelta(hours=1, minutes=1)
        otp.save()
        # Check that the save was successful
        self.assertFalse(otp.is_valid())

        self.assertFalse(otp.is_valid())

        otp.active = False
        otp.save()
        # self.assertFalse(otp.is_valid())
