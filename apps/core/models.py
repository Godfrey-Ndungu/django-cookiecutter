from django.db import models
from apps.accounts.models import CustomUser


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
        CustomUser, on_delete=models.PROTECT,
        related_name="%(class)s_created_by"
    )
    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT,
        related_name="%(class)s_updated_by"
    )

    class Meta:
        abstract = True


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
