from django.test import TestCase
from core.models import Task


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
