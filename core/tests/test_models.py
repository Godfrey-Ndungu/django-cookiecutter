from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone

from core.models import OTP
from core.models import Task


User = get_user_model()


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="Test Task",
            task_ingestor="Test Ingestor",
            status=Task.TASK_STATUS_PENDING,
        )

    def test_start_processing(self):
        self.task.start_processing()
        self.assertEqual(self.task.status, Task.TASK_STATUS_PROCESSING)

    def test_complete_processing(self):
        self.task.status = Task.TASK_STATUS_PROCESSING
        self.task.save()
        self.task.complete_processing()
        self.assertEqual(self.task.status, Task.TASK_STATUS_PROCESSED)

    def test_fail_processing(self):
        self.task.status = Task.TASK_STATUS_PROCESSING
        self.task.save()
        self.task.fail_processing()
        self.assertEqual(self.task.status, Task.TASK_STATUS_FAILED)

    def test_save_processed_task(self):
        self.task.status = Task.TASK_STATUS_PROCESSED
        self.task.save()
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())


class CustomUserManagerTests(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        user = User.objects.create_user(
            email=email, verification_code=verification_code, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.verification_code)

    def test_create_superuser(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        superuser = User.objects.create_superuser(
            email=email, verification_code=verification_code, password=password
        )

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.check_password(password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertFalse(superuser.is_active)
        self.assertIsNotNone(superuser.verification_code)

    def test_create_superuser_without_staff_flag(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=email,
                verification_code=verification_code,
                password=password,
                is_staff=False,
            )

    def test_create_superuser_without_superuser_flag(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=email,
                verification_code=verification_code,
                password=password,
                is_superuser=False,
            )

    def test_create_user_without_email(self):
        verification_code = "123456"
        password = "password123"
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email=None,
                verification_code=verification_code,
                password=password)

    def test_create_user_with_existing_email(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        User.objects.create_user(
            email=email, verification_code=verification_code, password=password
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email=email,
                verification_code=verification_code,
                password=password)

    def test_verify_code(self):
        email = "test@example.com"
        verification_code = "123456"
        password = "password123"
        user = User.objects.create_user(
            email=email, verification_code=verification_code, password=password
        )
        self.assertFalse(user.is_active)
        self.assertEqual(user.verification_code, verification_code)

        # Test with correct verification code
        self.assertTrue(user.verify_code(verification_code))
        self.assertTrue(user.is_active)
        self.assertIsNone(user.verification_code)

        # Test with incorrect verification code
        self.assertFalse(user.verify_code("654321"))
        self.assertTrue(user.is_active)
        self.assertIsNone(user.verification_code)


class OTPModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password="password",
            email="johndoe@example.com",
            verification_code="1234")

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
