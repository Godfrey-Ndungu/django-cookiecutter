from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

import uuid


class TrackableModel(models.Model):
    """
    Abstract model that provides fields
    to automatically track changes and keep a record of who made them.

    Attributes:
        created_at (DateTimeField): The timestamp when
            the model instance was first created.
        updated_at (DateTimeField): The timestamp of
            the most recent update to the model instance.
        created_by (ForeignKey): The user who created
            the model instance.
        updated_by (ForeignKey): The user who last updated
            the model instance.
        history (JSONField): A JSON field that stores a complete
            history of changes to the model instance,
            including timestamps and the user who made each change.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="%(class)s_updated_by"
    )
    history = JSONField(default=list, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the history
            field before saving the model instance.
        """
        if self.pk is None:
            self.history.append(
                {
                    "timestamp": self.created_at,
                    "user": self.created_by.id,
                    "action": "created",
                }
            )
        else:
            self.history.append(
                {
                    "timestamp": self.updated_at,
                    "user": self.updated_by.id,
                    "action": "updated",
                }
            )
        super().save(*args, **kwargs)


class TimestampedModel(TrackableModel):
    """
    Abstract model that builds on the functionality of
        TrackableModel by adding extra fields for timestamping.

    Attributes:
        date_added (DateTimeField): The timestamp when
            the model instance was first added.
        date_updated (DateTimeField): The timestamp of
            the most recent update to the model instance.
        date_deleted (DateTimeField): The timestamp of
            when the model instance was deleted (if applicable).
    """

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class SingletonModel(models.Model):
    """
    Abstract model that provides functionality for only
        allowing a single instance of a model to be created.

    Attributes:
        singleton_id (PositiveIntegerField):
            A field that stores the ID of the singleton instance.
            This field should always have a value of 1.
    """

    singleton_id = models.PositiveIntegerField(primary_key=True, default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overrides the save method to prevent multiple
            instances from being created.
        """
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Returns the singleton instance of the model.
            Creates the instance if it does not exist yet.
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Task(models.Model):
    """
    A model for tracking tasks.

    Attributes:
        name (str): The name of the task.
        task_ingestor (str): The ingestor responsible for the task.
        datetime (datetime): The date and time the task was created.
        status (str): The current status of the task.
            Allowed values are
            'pending', 'processing', 'processed', and 'failed'.
    """

    TASK_STATUS_PENDING = "pending"
    TASK_STATUS_PROCESSING = "processing"
    TASK_STATUS_PROCESSED = "processed"
    TASK_STATUS_FAILED = "failed"
    TASK_STATUS_CHOICES = (
        (TASK_STATUS_PENDING, "Pending"),
        (TASK_STATUS_PROCESSING, "Processing"),
        (TASK_STATUS_PROCESSED, "Processed"),
        (TASK_STATUS_FAILED, "Failed"),
    )

    name = models.CharField(max_length=255)
    task_ingestor = models.CharField(max_length=255, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=TASK_STATUS_CHOICES, default=TASK_STATUS_PENDING
    )

    def start_processing(self):
        """Transition the task from 'pending' to 'processing'."""
        if self.status == self.TASK_STATUS_PENDING:
            self.status = self.TASK_STATUS_PROCESSING
            self.save()

    def complete_processing(self):
        """Transition the task from 'processing'
        to 'processed' and delete the record."""
        if self.status == self.TASK_STATUS_PROCESSING:
            self.status = self.TASK_STATUS_PROCESSED
            self.save()

    def fail_processing(self):
        """Transition the task from 'processing' to 'failed'."""
        if self.status == self.TASK_STATUS_PROCESSING:
            self.status = self.TASK_STATUS_FAILED
            self.save()

    def save(self, *args, **kwargs):
        """Save the task"""
        super(Task, self).save(*args, **kwargs)


class UserVisitHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255)
    referer = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.TextField()

    class Meta:
        verbose_name_plural = "User visit history"
        ordering = ["-timestamp"]


class LoginHistoryTrail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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


class CustomUserManager(BaseUserManager):
    def create_user(
            self,
            email,
            verification_code,
            password=None,
            **extra_fields):
        """
        Creates and saves a User with the given email and verification code.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.verification_code = verification_code
        user.save()
        return user

    def create_superuser(
            self,
            email,
            verification_code,
            password=None,
            **extra_fields):
        """
        Creates and saves a superuser with the given
            email and verification code.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            email,
            verification_code,
            password,
            **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["verification_code"]

    def __str__(self):
        return self.email

    def verify_code(self, code):
        """
        Verify the verification code entered by user.
        """
        if self.verification_code == code:
            self.verification_code = None
            self.is_active = True
            self.save()
            return True
        return False


class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)

    @classmethod
    def create(cls, user):
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
        return cls.objects.filter(user=user,
                                  active=True).order_by('-created_at').first()

    def is_valid(self):
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
        # Mark any existing OTPs for this user as inactive
        OTP.objects.filter(user=self.user).update(active=False)

        # Validate that the code is a 4-digit number
        if not self.code.isdigit() or len(self.code) != 4:
            raise ValidationError('Invalid OTP code')

        super().save(*args, **kwargs)
