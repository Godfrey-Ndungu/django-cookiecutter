from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin

import uuid


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email
    is the unique identifier for authentication
    instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that extends Django's built-in User model.

    Fields:
        email: The user's email address (unique).
        phone_number: The user's phone number (optional).
        is_active: Whether the user account is active.
        is_staff: Whether the user is a member of the staff.
        is_superuser: Whether the user has all permissions.
        date_joined: The date and time the user account was created.

    Attributes:
        USERNAME_FIELD: The field to use for authentication
            (email in this case).
        REQUIRED_FIELDS: A list of required fields for creating a user.

    Methods:
        __str__: Returns the user's email address.

    Managers:
        objects: The manager for this model.

    Meta:
        verbose_name: A human-readable name for this model (singular).
        verbose_name_plural: A human-readable name for this model (plural).
    """

    email = models.EmailField(verbose_name="Email", unique=True)
    phone_number = models.CharField(
        verbose_name="Phone Number", max_length=15, blank=True
    )

    # Fields required by Django
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Fields used for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return self.email


class UserVisitHistory(models.Model):
    """
    Model to store the history of user visits to the site.

    Fields:
        user: A foreign key to the user who made the visit.
        timestamp: The date and time of the visit.
        url: The URL of the page visited.
        referer: The URL of the referring page, if any.
        user_agent: The user agent string for the browser
            or other client used to make the visit.

    Meta:
        verbose_name_plural: A human-readable name for this model (plural).
        ordering: The default ordering for querysets of this model,
            by timestamp in descending order.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255)
    referer = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.TextField()

    class Meta:
        verbose_name_plural = "User visit history"
        ordering = ["-timestamp"]


class LoginHistoryTrail(models.Model):
    """
    Model to store a trail of login attempts made by users.

    Fields:
        user: A foreign key to the user who made the login attempt.
        timestamp: The date and time of the login attempt.
        successful: Whether the login attempt was successful.
        ip_address: The IP address used to make the login attempt.
        user_agent: The user agent string for the browser or other client
            used to make the login attempt.
        location: The location (city, country) of the IP address used
            to make the login attempt, if available.

    Meta:
        verbose_name_plural: A human-readable name for this model (plural).
        ordering: The default ordering for querysets of this model,
            by timestamp in descending order.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Login history trail"
        ordering = ["-timestamp"]


class LoginAttemptsHistory(models.Model):
    """
    Model to store a history of login attempts made by users.

    Fields:
        user: A foreign key to the user who made the login attempt.
        timestamp: The date and time of the login attempt.
        successful: Whether the login attempt was successful.
        ip_address: The IP address used to make the login attempt.
        user_agent: The user agent string for the browser or
            other client used to make the login attempt.
        location: The location (city, country) of the IP
            address used to make the login attempt, if available.

    Meta:
        verbose_name_plural: A human-readable name for this model (plural).
        ordering: The default ordering for querysets of this model,
            by timestamp in descending order.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Login attempts history"
        ordering = ["-timestamp"]


class ExtraData(models.Model):
    """
    Model for storing extra data related to user activity, such as browser,
    IP address, device, operating system, and location.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    device = models.CharField(max_length=255, null=True, blank=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Extra data"
        ordering = ["-timestamp"]


class OTP(models.Model):
    """
    Model for storing one-time passwords (OTPs) associated with a user.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)

    @classmethod
    def create(cls, user):
        """
        Creates a new OTP for the given user.

        Args:
            user (CustomUser): The user associated with the new OTP.

        Returns:
            The newly created OTP.
        """

        # Mark all existing OTPs for the user as inactive
        cls.objects.filter(user=user).update(active=False)

        # Generate a unique 4-digit code
        while True:
            code = str(uuid.uuid4().int % 10000).zfill(4)
            if not cls.objects.filter(code=code).exists():
                break

        return cls.objects.create(user=user, code=code)

    @classmethod
    def get_latest(cls, user):
        """
        Gets the latest active OTP for the given user.

        Args:
            user (CustomUser): The user associated with the OTP.

        Returns:
            The latest active OTP, or None if there are no active OTPs.
        """

        return cls.objects.filter(user=user,
                                  active=True).order_by('-created_at').first()

    def is_valid(self):
        """
        Checks whether or not the OTP is valid (i.e. active and not expired).

        Returns:
            True if the OTP is valid, False otherwise.
        """
        # Check if the OTP is still active
        if not self.active:
            return False

        # Check if the OTP has expired
        expiration_time = self.updated_at + timezone.timedelta(hours=1)
        if timezone.now() > expiration_time:
            self.active = False
            self.save()
            return False

        return True

    def save(self, *args, **kwargs):
        """
        Saves the OTP to the database.

        Args:
            *args
            **kwargs

        Raises:
            ValidationError: If the code is not a 4-digit number.
        """

        # Mark any existing OTPs for this user as inactive
        OTP.objects.filter(user=self.user).update(active=False)

        # Validate that the code is a 4-digit number
        if not self.code.isdigit() or len(self.code) != 4:
            raise ValidationError('Invalid OTP code')

        super().save(*args, **kwargs)
